'''
This script allows you to choose a stream, the path to which can be found by
inspeciting webpage of the stream and look for an m3u8 file. In this case it is
chunklist.m3u8
'''
from pandemic51.core.download_stream import download_stream

output_path = "../out/video"

time_square_base_path = "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv"
ts_chunk = "chunklist.m3u8"


chicago_base_path = "https://videos-3.earthcam.com/fecnetwork/13220.flv"
chicago_chunk = "chunklist_w1227547844.m3u8"


download_stream(time_square_base_path, output_path, ts_chunk, "time_square")
#download_stream(chicago_base_path, output_path, chicago_chunk, "chicago")