'''
This script allows you to choose a stream, the path to which can be found by
inspecting the webpage of the stream and look for an m3u8 file. In this case it
is chunklist.m3u8
'''
from pandemic51.core.streaming import download_stream

output_path = "../out/video"

download_stream("time_square", output_path)
# download_stream("chicago", output_path)
