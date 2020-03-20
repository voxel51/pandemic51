'''
This script allows you to choose a stream, the path to which can be found by inspeciting webpage of the stream and look for an m3u8 file. In this case it is chunklist.m3u8


It requires you to install ffmpy: https://ffmpy.readthedocs.io/en/latest/ 

pip install ffmpy


And to install m3u8: https://github.com/globocom/m3u8

git clone https://github.com/globocom/m3u8
cd m3u8
python setup.py build
python setup.py install
'''

import ffmpy
import m3u8
import time
import os

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


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



output_path = "out"

time_square_base_path = "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv"
ts_chunk = "chunklist.m3u8"


chicago_base_path = "https://videos-3.earthcam.com/fecnetwork/13220.flv"
chicago_chunk = "chunklist_w1227547844.m3u8"


download_stream(time_square_base_path, output_path, ts_chunk, "time_square")
#download_stream(chicago_base_path, output_path, chicago_chunk, "chicago")

