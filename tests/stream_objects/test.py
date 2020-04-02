'''


Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.streaming as pans

outdir = "out"

# stream_name = "new_orleans"
stream_name = "time_square"

stream = pans.Stream.from_stream_name(stream_name)
stream.download_image_and_store(outdir)
