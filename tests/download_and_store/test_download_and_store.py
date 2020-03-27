'''
Test script for `pandemic51.core.streaming.download_and_store()`.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.streaming as pans


STREAM_NAMES = [
    "time_square", "chicago", "chicago_wrigleyville", "new_orleans",
    "new_jersey", "abbey_road", "dublin", "prague"]

OUT_BASEDIR = "out"


for stream_name in STREAM_NAMES:
    pans.download_and_store(stream_name, OUT_BASEDIR)
