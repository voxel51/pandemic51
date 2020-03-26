'''


'''
from datetime import datetime
import json
import os
import pathlib
import time

import ffmpy
import m3u8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import eta.core.serial as etas
import eta.core.utils as etau

import pandemic51.core.config as panc
from pandemic51.core.database import add_stream_history


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


def update_streams(stream_name, streams):
    ''''''
    chunk_path = get_chunk_info(streams[stream_name]["webpage"])
    streams[stream_name]["chunk_path"] = chunk_path
    etas.write_json(streams, panc.streams_path)
    return chunk_path


def get_chunk_info(webpage):
    '''Code from https://stackoverflow.com/questions/52633697/selenium-python-how-to-capture-network-traffics-response'''
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=caps)
    driver.get(webpage)
    
    attempts = 0
    chunk_url = None
    while chunk_url == None and attempts < 20:
        try:
            browser_log = driver.get_log('performance') 
            events = [process_browser_log_entry(entry)
                      for entry in browser_log]
            events = [event for event in events
                      if 'Network.response' in event['method']]
            
            for event in events:
                try:
                    url = event['params']['response']['url']
                    if "chunk" in url:
                        chunk_url = url
                except:
                    pass
        except:
            print("No performance")
            time.sleep(1)

    driver.service.stop()

    if chunk_url:
        return chunk_url
    
    else:
        raise TimeoutError(
            "Could not find the chunklist in the network traffic in time")


def save_video(uri, base_path, output_dir):
    ''''''
    out_name = os.path.splitext(uri)[0] + ".mp4"
    output_video_path = os.path.join(output_dir, out_name)
    etau.ensure_basedir(output_video_path)
    input_video = os.path.join(base_path, uri)

    cmd = ffmpy.FFmpeg(inputs={input_video: None},
                       outputs={output_video_path: None})
    cmd.run()

    return output_video_path


def download_chunk(stream_name, output_dir):
    ''''''
    streams = etas.load_json(panc.streams_path)
    chunk_path = streams[stream_name]["chunk_path"]
    base_path, chunk_name = os.path.split(chunk_path)

    output_path = os.path.join(output_dir, stream_name)

    uris = m3u8.load(chunk_path).segments.uri

    if not uris:
        chunk_path = update_streams(stream_name, streams)
        uris = m3u8.load(chunk_path).segments.uri
        
        if not uris:
            return None

    uri = uris[0]
    print("Processing uri ", uri)
    return save_video(uri, base_path, output_path), datetime.utcnow()


def download_stream(stream_name, output_dir, timeout=None):
    '''

    Args:
        stream_name:
        output_dir:
        timeout: duration (in seconds) to continue streaming. If None,
            continue forever
    '''
    streams = etas.load_json(panc.streams_path)
    chunk_path = streams[stream_name]["chunk_path"]
    base_path, chunk_name = os.path.split(chunk_path)

    output_path = os.path.join(output_dir, stream_name)

    processed_uris = []

    start = time.time()

    while (timeout is None or time.time()-start < timeout):
        time.sleep(1)
        uris = m3u8.load(chunk_path).segments.uri
        for uri in uris:
            if uri not in processed_uris:
                print("Processing uri ", uri)
                save_video(uri, base_path, output_path)
                processed_uris.append(uri)


def vid2img(inpath, outpath, width=None, height=None):
    '''Convert a video to a configurable-resolution image

    Args:
        inpath: input video path
        outpath: output png image path
        width:
        height: optional integer resizing options. If both are not specified,
            the default video dimensions are used
    '''
    if os.path.exists(outpath):
        return False

    etau.ensure_basedir(outpath)

    resize_param = "-s %dx%d" % (width, height) if width and height else ""

    outcmd = "-ss 00:00:00 -t 00:00:01 %s -r 1 -f image2" % resize_param

    cmd = ffmpy.FFmpeg(
        inputs={inpath:None },
        outputs={outpath: outcmd}
    )

    if not os.path.exists(outpath):
        cmd.run()

    return True


def download_and_store(
        stream_name, out_dir, tmpdirbase=None, width=None, height=None):
    '''Download an image from the latest stream, and add it to the database

    Returns:
        image_path: path the the downloaded image on disk
        dt: datetime object of when the image was downloaded
        tmpdirbase: base directory to create a tmpdir in
        width:
        height: optional integer resizing options. If both are not specified,
            the default video dimensions are used
    '''
    with etau.TempDir(basedir=tmpdirbase) as tmpdir:
        # download video
        video_path, dt = download_chunk(stream_name, tmpdir)

        # UTC integer timestamp (epoch time)
        timestamp = int(dt.timestamp())

        # create path for image
        vpath = pathlib.Path(video_path)
        image_path = os.path.join(
            out_dir, vpath.parent.stem, "%d.png" % timestamp)

        is_new_img = vid2img(video_path, image_path, width=width, height=height)

    if is_new_img:
        add_stream_history(stream_name, dt, image_path)

    return image_path, dt
