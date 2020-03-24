'''


'''
from datetime import datetime
import os
import pathlib
import time

import ffmpy
import m3u8

import eta.core.utils as etau

import pandemic51.core.config as p51c
from pandemic51.core.database import add_stream_history


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
    base_path = p51c.STREAMS[stream_name]["base_path"]
    chunk_name = p51c.STREAMS[stream_name]["chunk"]

    chunk_path = os.path.join(base_path, chunk_name)
    output_path = os.path.join(output_dir, stream_name)

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
    base_path = STREAMS[stream_name]["base_path"]
    chunk_name = STREAMS[stream_name]["chunk"]

    chunk_path = os.path.join(base_path, chunk_name)
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


def download_and_store(stream_name, out_dir, width=300, height=300):
    '''Download an image from the latest stream, and add it to the database'''
    with etau.TempDir(basedir=out_dir) as tmpdir:
        # download video
        video_path, timestamp = download_chunk(stream_name, tmpdir)

        # create path for image
        vpath = pathlib.Path(video_path)
        image_path = os.path.join(
            out_dir, vpath.parent.stem, vpath.stem + ".png")

        is_new_img = vid2img(video_path, image_path, width=width, height=height)

    if is_new_img:
        add_stream_history(stream_name, image_path, timestamp)
