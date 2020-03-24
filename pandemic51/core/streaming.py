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

from pandemic51.core.constants import streams_path
from pandemic51.core.database import add_stream_history


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


def update_streams(stream_name, STREAMS):
    ''''''
    chunk_path = get_chunk_info(STREAMS[stream_name]["webpage"])
    STREAMS[stream_name]["chunk_path"] = chunk_path
    etas.write_json(STREAMS, streams_path)
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
            events = [process_browser_log_entry(entry) for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]
            
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
        raise TimeoutError("Could not find the chunklist in the network traffic in time")


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
    STREAMS = etas.load_json(streams_path) 
    chunk_path = STREAMS[stream_name]["chunk_path"]
    #chunk_path = get_chunk_info(STREAMS[stream_name]["webpage"])
    base_path, chunk_name = os.path.split(chunk_path)

    output_path = os.path.join(output_dir, stream_name)

    uris = m3u8.load(chunk_path).segments.uri

    if not uris:
        chunk_path = update_streams(stream_name, STREAMS)
        uris = m3u8.load(chunk_path).segments.uri
        
        if not uris:
            return None

    uri = uris[0]
    print("Processing uri ", uri)
    return save_video(uri, base_path, output_path), datetime.now()


def download_stream(stream_name, output_dir, timeout=None):
    '''

    Args:
        stream_name:
        output_dir:
        timeout: duration (in seconds) to continue streaming. If None,
            continue forever
    '''
    STREAMS = etas.load_json(streams_path) 
    chunk_path = STREAMS[stream_name]["chunk_path"]
    #chunk_path = get_chunk_info(STREAMS[stream_name]["webpage"])
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


def vid2img(inpath, outpath, width=300, height=300):
    '''Convert a video to a configurable-resolution image'''
    if os.path.exists(outpath):
        return False

    etau.ensure_basedir(outpath)

    outcmd = "-ss 00:00:00 -t 00:00:01 -s %dx%d -r 1 -f image2" \
             % (width, height)

    cmd = ffmpy.FFmpeg(
        inputs={inpath:None },
        outputs={outpath: outcmd}
    )

    if not os.path.exists(outpath):
        cmd.run()

    return True


def download_and_store(stream_name, out_basedir, width=300, height=300):
    '''Download an image from the latest stream, and add it to the database'''
    with etau.TempDir(basedir=out_basedir) as tmpdir:
        # download video
        video_path, timestamp = download_chunk(stream_name, tmpdir)

        # create path for image
        vpath = pathlib.Path(video_path)
        image_path = os.path.join(
            out_basedir, "image", vpath.parent.stem, vpath.stem + ".png")

        is_new_img = vid2img(video_path, image_path, width=width, height=height)

    if is_new_img:
        print(video_path)
        print(image_path)
        print(timestamp)
        #add_stream_history(stream_name, image_path, timestamp)
