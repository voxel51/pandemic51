'''
Methods and Classes for downloading and working with video streams.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from datetime import datetime
import json
import logging
import os
import pathlib
from retrying import retry
import time
import urllib

from bs4 import BeautifulSoup
import ffmpy
import m3u8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

import eta.core.serial as etas
import eta.core.utils as etau

import pandemic51.config as panc
from pandemic51.core.database import add_stream_history


logger = logging.getLogger(__name__)


CHUNK_URL_MAX_NUM_ATTEMPTS = 20
CHUNK_URL_SLEEP_SECONDS = 1


def get_img_urls(webpage):
    '''Open the webpage and parse the source HTML for any image urls.

    Args:
        webpage: The webpage to scrape for image urls

    Returns:
        urls: List of url strings for all images in the webpage
    '''
    # Get the source from the page
    driver = _configure_webdriver()
    driver.get(webpage)

    # Ensure that all images have had time to load
    time.sleep(1)
    
    # Parse the source HTML for images with PSLNM in the title
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.service.stop()
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags]
    return urls


def save_video(chunk_path, uri, output_dir):
    '''Saves the video at the given URI to the given output directory.

    Args:
        chunk_path: the URL path for the chunklist
        uri: the video URI
        output_dir: the output directory

    Returns:
        the output video path
    '''
    base_path = os.path.split(chunk_path)[0]
    input_video = os.path.join(base_path, uri)
    out_name = os.path.splitext(uri)[0] + ".mp4"
    output_video_path = os.path.join(output_dir, out_name)

    etau.ensure_basedir(output_video_path)
    ffmpy.FFmpeg(
        inputs={input_video: None},
        outputs={output_video_path: None},
    ).run()

    return output_video_path


def sample_first_frame(inpath, outpath):
    '''Samples the first frame of the given video.

    Args:
        inpath: input video path
        outpath: the path to write the output image

    Returns:
        True if the image was created, or False if it already existed
    '''
    if os.path.exists(outpath):
        return False

    outcmd = "-ss 00:00:00 -t 00:00:01 -r 1 -f image2"

    etau.ensure_basedir(outpath)
    ffmpy.FFmpeg(
        inputs={inpath: None},
        outputs={outpath: outcmd},
    ).run()

    return True


class Stream(etas.Serializable):
    '''Abstract class for streams of various types providing functionality for
    downloading clips and images from the stream, getting the latest stream URL,
    etc.
    '''
    def __init__(self, stream_name, GMT):
        '''
        Args:
            stream_name: name of the stream (should match JSON file in
                {{pandemic51}}/config/streams/
            GMT: integer relative timezone of stream
        '''
        self.type = etau.get_class_name(self)
        self.stream_name = stream_name
        self.GMT = GMT

    @staticmethod
    def stream_path(stream_name):
        '''Get the path to the Stream JSON file.

        Args:
            stream_name: name of the stream

        Returns:
            path the the Stream object serialized on disk
        '''
        return os.path.join(panc.STREAMS_DIR, stream_name + ".json")

    @staticmethod
    def get_stream_names():
        '''Get names of all streams serialized on disk.

        Returns:
             a list of stream_name strings
        '''
        _, matches = etau.parse_glob_pattern(Stream.stream_path("*"))
        return [x[0] for x in matches]

    @property
    def path(self):
        '''Path to the Stream serialized on disk'''
        return self.stream_path(self.stream_name)

    def get_live_stream_url(self):
        '''Get the URL for streaming'''
        raise NotImplementedError("Subclass must implement")

    def download_image(self, outdir):
        '''Downloads an image from the latest stream

        Args:
            outdir: the output directory

        Returns:
            is_new_img: `True` if the image was not already on disk
            image_path: path the the downloaded image on disk
            dt: datetime object of when the image was downloaded
        '''
        raise NotImplementedError("Subclass must implement")

    def download_image_and_store(self, outdir):
        '''Downloads an image from the latest stream, and add it to the
        database.

        If an image with the same filename was already on disk, no new entry is
        added to the database.

        Args:
            stream_name: the stream name
            outdir: the output directory

        Returns:
            image_path: path the the downloaded image on disk
            dt: datetime object of when the image was downloaded
        '''
        is_new_img, image_path, dt = self.download_image(outdir)

        if is_new_img:
            add_stream_history(self.stream_name, dt, image_path)

        return image_path, dt

    @classmethod
    def from_dict(cls, d, *args, **kwargs):
        '''Constructs a Stream object from a JSON dictionary.

        Args:
            d: a JSON dictionary representation of a Serializable object

        Returns:
            a Stream instance
        '''
        downloader_cls = etau.get_class(d["type"])
        return downloader_cls._from_dict(d)

    @classmethod
    def from_json(cls, path, *args, **kwargs):
        '''Constructs a Stream object from a JSON file.

        If `stream_name` key is missing, it is automatically populated.

        Args:
            path: the path to the JSON file on disk

        Returns:
            a Stream instance
        '''
        d = etas.read_json(path)

        if "stream_name" not in d:
            d["stream_name"] = os.path.splitext(os.path.basename(path))[0]

        return cls.from_dict(d, *args, **kwargs)

    @classmethod
    def from_stream_name(cls, stream_name):
        '''Constructs a Stream object.

        Args:
            stream_name: the name of the stream

        Returns:
            a Stream instance
        '''
        return cls.from_json(cls.stream_path(stream_name))

    @classmethod
    def _from_dict(cls, d):
        raise NotImplementedError("Subclass must implement")


class M3U8Stream(Stream):
    '''A Stream class that reads URIs from an M3U8 chunk path'''
    def __init__(self, stream_name, GMT, webpage, chunk_path):
        super(M3U8Stream, self).__init__(stream_name, GMT)
        self.webpage = webpage
        self.chunk_path = chunk_path

    def get_live_stream_url(self):
        url = self.chunk_path

        try:
            urllib.request.urlopen(url)
        except urllib.error.HTTPError:
            self.update_stream_chunk_path()
            url = self.chunk_path

        if "videos2archives" in url:
            url = (
                    "https://pdi-service.voxel51.com/stream-archive/" +
                    url.split(".com/")[1]
            )
        elif "earthcam" in url:
            url = (
                    "https://pdi-service.voxel51.com/stream/" +
                    url.split(".com/")[1]
            )

        return url

    def download_image(self, outdir):
        '''Downloads an image from the latest stream

        Args:
            outdir: the output directory

        Returns:
            is_new_img: `True` if the image was not already on disk
            image_path: path the the downloaded image on disk
            dt: datetime object of when the image was downloaded
        '''
        with etau.TempDir(basedir=panc.BASE_DIR) as tmpdir:
            # Download video
            video_path, dt = self.download_chunk(tmpdir)

            # UTC integer timestamp (epoch time)
            timestamp = int(dt.timestamp())

            # Create path for image
            image_path = os.path.join(
                outdir, self.stream_name, "%d.jpg" % timestamp)

            is_new_img = sample_first_frame(video_path, image_path)

        return is_new_img, image_path, dt

    def download_chunk(self, output_dir):
        '''Downloads a chunk of the given stream to the given directory.

        Args:
            output_dir: the output directory
        '''
        output_path = os.path.join(output_dir, self.stream_name)

        uris = self.get_uris()
        uri = uris[-1]

        logger.info("Processing URI '%s'", uri)
        return save_video(self.chunk_path, uri, output_path), datetime.utcnow()

    @retry(stop_max_attempt_number=10, wait_fixed=100)
    def get_uris(self):
        '''Attempts to load uris from a given chunk path. Will handle HTTPS
        Errors and update the chunk path.

        Args:
            chunk_path: URL of the chunklist to attempt to load
            stream_name: name of the stream corresponding to chunk_path

        Returns:
            uris: the uris present in the chunk_path
        '''
        try:
            uris = self._attempt_get_uris()
            if not uris:
                self.update_stream_chunk_path()
                uris = self._attempt_get_uris()

        except urllib.error.HTTPError:
            self.update_stream_chunk_path()
            uris = self._attempt_get_uris()

        return uris

    def update_stream_chunk_path(self):
        '''Updates the given stream in the stream dictionary and serializes it
        to disk in `pandemic51.config.STREAMS_DIR`.

        Args:
            stream_name: the stream name

        Returns:
            the chunk path
        '''
        self.chunk_path = _get_chunk_url(self.webpage)
        self.write_json(self.path, pretty_print=True)

    def _attempt_get_uris(self):
        return m3u8.load(self.chunk_path).segments.uri

    @classmethod
    def _from_dict(cls, d):
        stream_name = d["stream_name"]
        GMT = d["GMT"]
        webpage = d["webpage"]
        chunk_path = d["chunk_path"]
        return cls(stream_name, GMT, webpage, chunk_path)


class MjpegStream(Stream):
    '''A Stream class that reads MJPEGs'''
    def __init__(self, stream_name, GMT, url):
        super(MjpegStream, self).__init__(stream_name, GMT)
        self.url = url

    def get_live_stream_url(self):
        '''Get the URL for streaming'''
        # @todo(Tyler)
        raise NotImplementedError("TODO")

    def download_image(self, outdir):
        '''Downloads an image from the latest stream

        Args:
            outdir: the output directory

        Returns:
            is_new_img: `True` if the image was not already on disk
            image_path: path the the downloaded image on disk
            dt: datetime object of when the image was downloaded
        '''
        dt = datetime.utcnow()

        # UTC integer timestamp (epoch time)
        timestamp = int(dt.timestamp())

        # Create path for image
        image_path = os.path.join(
            outdir, self.stream_name, "%d.jpg" % timestamp)
        etau.ensure_basedir(image_path)

        # Capture the current frame of the stream
        is_new_img = sample_first_frame(self.url, image_path)

        return is_new_img, image_path, dt

    @classmethod
    def _from_dict(cls, d):
        stream_name = d["stream_name"]
        GMT = d["GMT"]
        url = d["url"]
        return cls(stream_name, GMT, url)


class ImageStream(Stream):
    '''A Stream class for streams that intermittently take image snapshots,
    rather than providing constant video feed.
    '''
    # @todo(Tyler)
    pass


def _get_chunk_url(webpage):
    driver = _configure_webdriver()
    driver.get(webpage)

    chunk_url = None
    num_attempts = 0
    while chunk_url is None and num_attempts < CHUNK_URL_MAX_NUM_ATTEMPTS:
        try:
            browser_log = driver.get_log("performance")
            events = [
                _process_browser_log_entry(entry) for entry in browser_log]
            events = [
                e for e in events if "Network.response" in e["method"]]

            for event in events:
                try:
                    url = event["params"]["response"]["url"]
                    if "chunk" in url:
                        chunk_url = url
                except:
                    pass
        except:
            num_attempts += 1
            logger.info("Failed to get chunk URL from '%s'", webpage)
            time.sleep(CHUNK_URL_SLEEP_SECONDS)

    driver.service.stop()

    if chunk_url:
        return chunk_url

    raise TimeoutError(
        "Failed to get the chunklist from the network traffic")


def _process_browser_log_entry(entry):
    return json.loads(entry["message"])["message"]


def _configure_webdriver():
    # Reference: https://stackoverflow.com/q/52633697
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        desired_capabilities=caps, options=chrome_options,
        executable_path="/usr/bin/chromedriver")
    return driver
