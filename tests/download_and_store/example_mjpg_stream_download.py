'''
Example script for downloading mjpg streams in realtime as a sequence of
frames. This will continue to download until a termination signal is recieved
(Ctrl+C). 

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
from datetime import datetime
import os

import ffmpy

import eta.core.utils as etau
import pandemic51.core.streaming as pans


def stream_frames(input_video, base_output_dir):
    output_frames_path = os.path.join("out", base_output_dir, "%Y-%m-%d_%H-%M-%S.jpg")
    etau.ensure_basedir(output_frames_path)
    
    ffmpy.FFmpeg(
        inputs={input_video: None},
        outputs={output_frames_path: "-strftime 1"},
    ).run()


# Ann Arbor
input_video = "http://141.213.137.162/mjpg/video.mjpg"
base_output_dir = "ann_arbor"

## Detroit
#input_video = "http://216.8.159.21/axis-cgi/mjpg/video.cgi"
#base_output_dir = "detroit"


# Capture the current frame of the stream
output_frames_path = os.path.join("out", base_output_dir,
        str(datetime.now()).replace(" ", "_")+".jpg")
etau.ensure_basedir(output_frames_path)

pans.sample_first_frame(input_video, output_frames_path)


## Continually stream frames as images
#stream_frames(input_video, base_output_dir)

