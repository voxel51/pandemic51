'''
Methods and Classes for downloading and working with video streams.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from __future__ import unicode_literals
from datetime import datetime
import io
import json
import logging
import os
import requests
from retrying import retry
import time
import urllib

from bs4 import BeautifulSoup
import ffmpy
import m3u8
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from youtube_dl import YoutubeDL

import eta.core.image as etai
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
    if "earthcam" in chunk_path:
        res = requests.get(
            input_video,
            headers={
                "Host": "https://www.earthcam.com",
                "Referrer": "https://www.earthcam.com/"
            }
        )
        input_video = "./temp.ts"
        with open(input_video, "wb") as ff:
            ff.write(res.content)

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
            image_path: path to the downloaded image on disk
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
    def __init__(self, stream_name, GMT, webpage):
        super(M3U8Stream, self).__init__(stream_name, GMT)
        self.webpage = webpage

    def get_live_stream_url(self):
        url = _get_chunk_url(self.webpage)

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

            if not video_path:
                # this is archival data, so don't return an image
                return False, None, dt

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

        Returns:
            tuple of:
                - path to the downloaded video chunk
                    OR None if the stream is an archive stream
                - the datetime when the video chunk was downloaded
        '''
        output_path = os.path.join(output_dir, self.stream_name)

        uris, chunk_path = self.get_uris_and_chunk_path()

        if "archive" in chunk_path:
            return None, datetime.utcnow()

        uri = uris[-1]

        logger.info("Processing URI '%s'", uri)
        return save_video(chunk_path, uri, output_path), datetime.utcnow()

    @retry(stop_max_attempt_number=10, wait_fixed=100)
    def get_uris_and_chunk_path(self):
        '''Attempts to load uris from a given chunk path. Will handle HTTPS
        Errors and update the chunk path.

        Args:
            chunk_path: URL of the chunklist to attempt to load
            stream_name: name of the stream corresponding to chunk_path

        Returns:
            uris: the uris present in the chunk_path
        '''
        chunk_path = _get_chunk_url(self.webpage)
        try:
            uris = m3u8.load(chunk_path).segments.uri
            if not uris:
                chunk_path = _get_chunk_url(self.webpage)
                uris = m3u8.load(chunk_path).segments.uri

        except urllib.error.HTTPError:
            chunk_path = _get_chunk_url(self.webpage)
            uris = m3u8.load(chunk_path).segments.uri

        return uris, chunk_path

    @classmethod
    def _from_dict(cls, d):
        stream_name = d["stream_name"]
        GMT = d["GMT"]
        webpage = d["webpage"]
        return cls(stream_name, GMT, webpage)


class MjpegStream(Stream):
    '''A Stream class that reads MJPEGs'''
    def __init__(self, stream_name, GMT, url):
        super(MjpegStream, self).__init__(stream_name, GMT)
        self.url = url

    def get_live_stream_url(self):
        '''Get the URL for streaming'''
        return self.url

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

    def __init__(self, stream_name, GMT, webpage, url_filter):
        super(ImageStream, self).__init__(stream_name, GMT)
        self.webpage = webpage
        self.url_filter = url_filter

    def get_live_stream_url(self):
        '''Get the URL for streaming'''
        # Get the source from the page
        urls = get_img_urls(self.webpage)
        filtered_urls = [u for u in urls if self.url_filter in u]

        if not filtered_urls:
            raise Exception("No URLs found for webpage: %s" % self.webpage)

        # we only need one!
        url = filtered_urls[0]

        # Get the large version of the image instead of the thumbnail
        url = url[:-5] + "l" + url[-4:]

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
        url = self.get_live_stream_url()
        img = self._load_image_from_url(url)
        dt = self._parse_datetime(url)

        # UTC integer timestamp (epoch time)
        timestamp = int(dt.timestamp())

        # Create path for image
        image_path = os.path.join(
            outdir, self.stream_name, "%d.jpg" % timestamp)
        etau.ensure_basedir(image_path)

        if os.path.exists(image_path):
            is_new_img = False
        else:
            is_new_img = True
            etai.write(img, image_path)

        return is_new_img, image_path, dt

    def _load_image_from_url(self, url):
        data = requests.get(url).content
        return np.array(Image.open(io.BytesIO(data)))

    def _parse_datetime(self, url):
        time_str = url.split("/")[-1].split("_")[0]
        return datetime.strptime(time_str, "%m%d%Y%H%M")

    @classmethod
    def _from_dict(cls, d):
        stream_name = d["stream_name"]
        GMT = d["GMT"]
        webpage = d["webpage"]
        url_filter = d["url_filter"]
        return cls(stream_name, GMT, webpage, url_filter)


class YouTubeStream(Stream):
    '''A Stream class for YouTube live-streams.'''

    def __init__(self, stream_name, GMT, youtube_id):
        super(YouTubeStream, self).__init__(stream_name, GMT)
        self.youtube_id = youtube_id
        self._m3u8 = None

    def get_live_stream_url(self):
        '''Returns the livestream URL.'''
        return "https://www.youtube.com/embed/%s?autoplay=1" % self.youtube_id

    def get_m3u8_url(self, force=False):
        '''Returns the current best m3u8 stream.'''
        if force or self._m3u8 is None:
            ydl_opts = {}
            with YoutubeDL(ydl_opts) as ydl:
                yyy = ydl.extract_info(self.youtube_id, download=False)
            self._m3u8 = yyy['url']
        return self._m3u8

    def download_image(self, outdir):
        '''Downloads an image from the stream

        Args:
            outdir: the output directory

        Returns:
            is_new_img: `True` if the image was not already on disk
            image_path: path to the downloaded image on disk
            dt: datetime object of when the image was downloaded
        '''
        m3u8_url = self.get_m3u8_url()

        dt = datetime.utcnow()

        # UTC integer timestamp (epoch time)
        ts = int(dt.timestamp())

        # Create path for image
        image_path = os.path.join(outdir, self.stream_name, "%d.jpg" % ts)

        # Capture the current frame of the stream
        is_new_img = sample_first_frame(m3u8_url, image_path)

        return is_new_img, image_path, dt

    @classmethod
    def _from_dict(cls, d):
        stream_name = d["stream_name"]
        GMT = d["GMT"]
        youtube_id = d["youtube_id"]
        return cls(stream_name, GMT, youtube_id)


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
