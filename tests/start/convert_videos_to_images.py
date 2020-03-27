'''
Test converting a video to a configurable-resolution image.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
import glob
import os

import pandemic51.core.streaming as pans


INPUT_PATTERN = "out/video/time_square/*.mp4"
OUT_DIR = "out/img/time_square"

for input_path in glob.glob(INPUT_PATTERN):
    outfilename = os.path.splitext(os.path.basename(input_path))[0] + ".png"
    out_path = os.path.join(OUT_DIR, outfilename)

    pans.sample_first_frame(input_path, out_path)
