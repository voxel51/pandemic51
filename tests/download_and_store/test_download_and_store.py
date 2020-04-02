'''
Test script for `pandemic51.core.streaming.Stream.download_image_and_store()`.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.streaming as pans


STREAM_NAMES = [
    "time_square", "chicago", "new_orleans", "fort_lauderdale",
    "new_jersey", "abbey_road", "dublin", "prague"]

OUT_BASEDIR = "out"


for stream_name in STREAM_NAMES:
    stream = pans.Stream.from_stream_name(stream_name)
    stream.download_image_and_store(outdir=OUT_BASEDIR)
