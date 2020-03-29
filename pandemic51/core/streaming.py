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
import time

import ffmpy
import m3u8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import eta.core.serial as etas
import eta.core.utils as etau

import pandemic51.config as panc
from pandemic51.core.database import add_stream_history


logger = logging.getLogger(__name__)


CHUNK_URL_MAX_NUM_ATTEMPTS = 20
CHUNK_URL_SLEEP_SECONDS = 1


def update_streams(stream_name, streams):
    '''Updates the given stream in the stream dictionary and serializes it to
    disk at `pandemic51.config.STREAMS_PATH`.

    Args:
        stream_name: the stream name
        streams: the current dict of stream info

    Returns:
        the chunk path
    '''
    chunk_path = _get_chunk_url(streams[stream_name]["webpage"])
    streams[stream_name]["chunk_path"] = chunk_path
    etas.write_json(streams, panc.STREAMS_PATH)
    return chunk_path


def _get_chunk_url(webpage):
    # Reference: https://stackoverflow.com/q/52633697
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(desired_capabilities=caps)
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


def save_video(base_path, uri, output_dir):
    '''Saves the video at the given URI to the given output directory.

    Args:
        base_path: the base path for the video URI
        uri: the video URI
        output_dir: the output directory

    Returns:
        the output video path
    '''
    input_video = os.path.join(base_path, uri)
    out_name = os.path.splitext(uri)[0] + ".mp4"
    output_video_path = os.path.join(output_dir, out_name)

    etau.ensure_basedir(output_video_path)
    ffmpy.FFmpeg(
        inputs={input_video: None},
        outputs={output_video_path: None},
    ).run()

    return output_video_path


def download_chunk(stream_name, output_dir):
    '''Downloads a chunk of the given stream to the given directory.

    Args:
        stream_name: the stream name
        output_dir: the output directory
    '''
    streams = etas.load_json(panc.STREAMS_PATH)
    chunk_path = streams[stream_name]["chunk_path"]
    base_path = os.path.split(chunk_path)[0]
    output_path = os.path.join(output_dir, stream_name)

    uris = m3u8.load(chunk_path).segments.uri

    if not uris:
        chunk_path = update_streams(stream_name, streams)
        uris = m3u8.load(chunk_path).segments.uri

        if not uris:
            return None

    uri = uris[0]

    logger.info("Processing URI '%s'", uri)
    return save_video(base_path, uri, output_path), datetime.utcnow()


def download_stream(stream_name, output_dir, timeout=None):
    '''Downloads the given stream.

    Args:
        stream_name: the stream name
        output_dir: the output directory
        timeout: duration (in seconds) to continue streaming. If None, continue
            forever
    '''
    streams = etas.load_json(panc.STREAMS_PATH)
    chunk_path = streams[stream_name]["chunk_path"]
    base_path = os.path.split(chunk_path)[0]
    output_path = os.path.join(output_dir, stream_name)

    processed_uris = []

    start = time.time()
    while timeout is None or (time.time() - start < timeout):
        time.sleep(1)
        uris = m3u8.load(chunk_path).segments.uri
        for uri in uris:
            if uri not in processed_uris:
                logger.info("Processing URI '%s'", uri)
                save_video(base_path, uri, output_path)
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
    with etau.TempDir() as tmpdir:
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
