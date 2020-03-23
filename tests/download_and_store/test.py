'''
Download and Store


This script tests the function `download_and_store`, which:
    1) downloads a single image from a video stream
    2) saves it to disk
    3) adds and entry to the database table `stream_history` referring to this
        sample

still TODO:
4) inference (for every empty "labels" column)
5) store labels to DB
'''
from pandemic51.core.streaming import download_and_store


stream_name = "time_square"
# stream_name = "chicago"

out_basedir = "out"

download_and_store(stream_name, out_basedir)
