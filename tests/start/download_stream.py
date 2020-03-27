'''
This script allows you to download streams from earthcam.com in real time.
It will download videos roughly 6 seconds long and save them as `.mp4` files.

In order to get downloads for a new stream, you need to inspect element on the
videos page and go to the network tab. Look for `chunklist.m3u8` and copy the
link address to that file.

This file contains the information of which clips to load.

The actual clips themselves are the `media_XXXX.ts` files.

This script allows you to choose a stream, the path to which can be found by
inspecting the webpage of the stream and look for an m3u8 file. In this case it
is chunklist.m3u8.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.streaming as pans


STREAM_NAME = "time_square"
# STREAM_NAME = "chicago"

OUTPUT_DIR = "out/video"

TIMEOUT = 10


pans.download_stream(
    stream_name=STREAM_NAME, output_dir=OUTPUT_DIR, timeout=TIMEOUT)
