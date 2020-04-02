'''
Test script for `pandemic51.core.streaming.Stream.download_image_and_store()`.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.streaming as pans


OUT_BASEDIR = "out"


for stream_name in pans.Stream.get_stream_names():
    stream = pans.Stream.from_stream_name(stream_name)
    stream.download_image_and_store(outdir=OUT_BASEDIR)
