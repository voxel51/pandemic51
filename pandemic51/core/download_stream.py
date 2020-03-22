'''


'''
import os
import time

import ffmpy
import m3u8

from pandemic51.core.utils import ensure_dir


def save_video(uri, base_path, output_path):
    out_name = os.path.splitext(uri)[0]+".mp4"
    output_video_path = os.path.join(output_path, out_name)
    ensure_dir(output_video_path)
    input_video = os.path.join(base_path, uri)

    cmd = ffmpy.FFmpeg(inputs={input_video: None}, outputs={output_video_path: None})
    cmd.run()


def download_stream(base_path, output_path, chunk_name, stream_name):
    chunk_path = os.path.join(base_path, chunk_name)
    output_path = os.path.join(output_path, stream_name)
    
    processed_uris = []
    
    while True: 
        time.sleep(1)
        uris = m3u8.load(chunk_path).segments.uri
        for uri in uris:
            if uri not in processed_uris:
                print("Processing uri ", uri)
                save_video(uri, base_path, output_path)
                processed_uris.append(uri)
