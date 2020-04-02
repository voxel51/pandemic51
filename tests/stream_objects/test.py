'''Example for sampling an image from each stream in the config using the
serializable pandemic51.core.streaming.Stream class


Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.streaming as pans

outdir = "out"

stream_names = pans.Stream.get_stream_names()

for stream_name in stream_names:
    print("Downloading %s" % stream_name)
    stream = pans.Stream.from_stream_name(stream_name)
    stream.download_image_and_store(outdir)
