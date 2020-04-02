'''
Methods for downloading and working with video streams.

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
from urllib.error import HTTPError

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


def update_stream_chunk_path(stream_name):
    '''Updates the given stream in the stream dictionary and serializes it to
    disk at `pandemic51.config.STREAMS_PATH`.

    Args:
        stream_name: the stream name

    Returns:
        the chunk path
    '''
    streams = etas.load_json(panc.STREAMS_PATH)
    chunk_path = _get_chunk_url(streams[stream_name]["webpage"])
    streams[stream_name]["chunk_path"] = chunk_path
    etas.write_json(streams, panc.STREAMS_PATH, pretty_print=True)
    return chunk_path


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

    raise TimeoutError("Failed to get the chunklist from the network traffic")


def _process_browser_log_entry(entry):
    return json.loads(entry["message"])["message"]


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


def download_stream(stream_name, output_dir, timeout=None):
    '''Downloads the given stream.

    Args:
        stream_name: the stream name
        output_dir: the output directory
        timeout: duration (in seconds) to continue streaming. If None, continue
            forever
    '''
    output_path = os.path.join(output_dir, stream_name)

    processed_uris = []

    start = time.time()
    while timeout is None or (time.time() - start < timeout):
        time.sleep(1)
        chunk_path, uris = _get_chunk_path_and_uris(stream_name)
        for uri in uris:
            if uri not in processed_uris:
                logger.info("Processing URI '%s'", uri)
                save_video(chunk_path, uri, output_path)
                processed_uris.append(uri)


def sample_first_frame(inpath, outpath, width=None, height=None):
    '''Samples the first frame of the given video.

    Args:
        inpath: input video path
        outpath: the path to write the output image
        width: an optional width to resize the image
        height: an optional height to resize the image

    Returns:
        True if the image was created, or False if it already existed
    '''
    if os.path.exists(outpath):
        return False

    resize_param = "-s %dx%d" % (width, height) if width and height else ""
    outcmd = "-ss 00:00:00 -t 00:00:01 %s -r 1 -f image2" % resize_param

    etau.ensure_basedir(outpath)
    ffmpy.FFmpeg(
        inputs={inpath: None},
        outputs={outpath: outcmd},
    ).run()

    return True


def download_and_store(stream_name, outdir, width=None, height=None):
    '''Downloads an image from the latest stream, and add it to the database.

    Args:
        stream_name: the stream name
        outdir: the output directory
        width: an optional width to resize the image
        height: an optional height to resize the image

    Returns:
        image_path: path the the downloaded image on disk
        dt: datetime object of when the image was downloaded
    '''
    with etau.TempDir(basedir=panc.BASE_DIR) as tmpdir:
        # Download video
        video_path, dt = download_chunk(stream_name, tmpdir)

        # UTC integer timestamp (epoch time)
        timestamp = int(dt.timestamp())

        # Create path for image
        vpath = pathlib.Path(video_path)
        image_path = os.path.join(
            outdir, vpath.parent.stem, "%d.png" % timestamp)

        is_new_img = sample_first_frame(
            video_path, image_path, width=width, height=height)

    if is_new_img:
        add_stream_history(stream_name, dt, image_path)

    return image_path, dt


class Stream(etas.Serializable):
    def __init__(self, stream_name, GMT):
        self.type = etau.get_class_name(self)
        self.stream_name = stream_name
        self.GMT = GMT

    def download_image(self, outdir, overwrite=False):
        raise NotImplementedError("Subclass must implement")

    def get_m3u8_stream(self):
        # @todo(Tyler)
        raise NotImplementedError("TODO")

    @classmethod
    def from_dict(cls, d, *args, **kwargs):
        downloader_cls = etau.get_class(d["type"])
        return downloader_cls._from_dict(d)

    @classmethod
    def from_json(cls, path, *args, **kwargs):
        d = etas.read_json(path)

        if "stream_name" not in d:
            d["stream_name"] = os.path.splitext(os.path.basename(path))[0]

        return cls.from_dict(d, *args, **kwargs)


    @classmethod
    def from_stream_name(cls, stream_name):
        stream_path = os.path.join(panc.STREAMS_DIR, stream_name + ".json")
        return cls.from_json(stream_path)


    @classmethod
    def _from_dict(cls, d):
        raise NotImplementedError("Subclass must implement")


class M3U8Stream(Stream):
    def __init__(self, stream_name, GMT, webpage, chunk_path):
        super(M3U8Stream, self).__init__(stream_name, GMT)
        self.webpage = webpage
        self.chunk_path = chunk_path


    def download_image(self, outdir, overwrite=False, width=None, height=None):
        with etau.TempDir(basedir=panc.BASE_DIR) as tmpdir:
            # Download video
            video_path, dt = self.download_chunk(tmpdir)

            # UTC integer timestamp (epoch time)
            timestamp = int(dt.timestamp())

            # Create path for image
            vpath = pathlib.Path(video_path)
            image_path = os.path.join(
                outdir, vpath.parent.stem, "%d.png" % timestamp)

            is_new_img = sample_first_frame(
                video_path, image_path, width=width, height=height)

    def download_chunk(self, output_dir):
        '''Downloads a chunk of the given stream to the given directory.

        Args:
            output_dir: the output directory
        '''
        output_path = os.path.join(output_dir, self.stream_name)

        chunk_path, uris = self._get_chunk_path_and_uris()
        uri = uris[-1]

        logger.info("Processing URI '%s'", uri)
        return save_video(chunk_path, uri, output_path), datetime.utcnow()

    @retry(stop_max_attempt_number=10, wait_fixed=100)
    def _get_chunk_path_and_uris(self):
        '''Attempts to load uris from a given chunk path. Will handle HTTPS
        Errors and update the chunk path.

        Args:
            chunk_path: URL of the chunklist to attempt to load
            stream_name: name of the stream corresponding to chunk_path

        Returns:
            uris: the uris present in the chunk_path
        '''
        streams = etas.load_json(panc.STREAMS_PATH)
        chunk_path = streams[self.stream_name]["chunk_path"]

        try:
            uris = m3u8.load(chunk_path).segments.uri
            if not uris:
                chunk_path = update_stream_chunk_path(self.stream_name)
                uris = m3u8.load(chunk_path).segments.uri

        except HTTPError:
            chunk_path = update_stream_chunk_path(self.stream_name)
            uris = m3u8.load(chunk_path).segments.uri

        return chunk_path, uris

    @classmethod
    def _from_dict(cls, d):
        stream_name = d["stream_name"]
        GMT = d["GMT"]
        webpage = d["webpage"]
        chunk_path = d["chunk_path"]
        return cls(stream_name, GMT, webpage, chunk_path)


class MjpegStream(Stream):
    pass


class ImageStream(Stream):
    pass
