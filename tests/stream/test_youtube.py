'''
Test script for `pandemic51.core.streaming.YouTubeStream`

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.streaming as pans


OUT_BASEDIR = "/tmp"


print("Creating the stream")

stream = pans.Stream.from_json("./youtube-test.json")

print(stream)

print("The livestream URL for embedding is: %s" % stream.get_live_stream_url())

print("The m3u8 stream URL is: %s" % stream.get_m3u8_url())

print("Getting an image")

path, dt = stream.download_image_and_store(outdir=OUT_BASEDIR)

print("Stored it at %s" % path)

print("The m3u8 stream URL is: %s" % stream.get_m3u8_url(force=True))

print("Done")
