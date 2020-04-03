'''
Test script for `pandemic51.core.streaming.Stream.download_image_and_store()`.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.streaming as pans


OUT_BASEDIR = "out"

# STREAM_NAMES = pans.Stream.get_stream_names()
STREAM_NAMES = ["detroit"]

for stream_name in STREAM_NAMES:
    stream = pans.Stream.from_stream_name(stream_name)
    stream.download_image_and_store(outdir=OUT_BASEDIR)
