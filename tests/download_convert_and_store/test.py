'''
1) Download single video streams in DB.streams.
2) Convert to Image
3) add to database
...
4) inference (for every empty "labels" column)
5) store labels to DB

'''
import pathlib

from pandemic51.core.streaming import download_chunk, vid2img, download_and_store
from pandemic51.core.database import add_stream_history


stream_name = "time_square"
# stream_name = "chicago"

out_basedir = "../out"

# video_path, timestamp = download_chunk(stream_name, output_dir)
#
# print(video_path)
#
# vpath = pathlib.Path(video_path)
#
# image_path = str(vpath.parent.parent.parent.joinpath(
#     "image", vpath.parent.stem, vpath.stem + ".png"))
#
# if vid2img(video_path, image_path, width=300, height=300):
#     add_stream_history(stream_name, image_path, timestamp)

download_and_store(stream_name, out_basedir)


'''
PARAMS
- list streams
- specify sampling interval
- specify initial time
'''

'''
CODE
- get all "desired" timestamps
- get images for all of these (that are missing)
'''

'''
CELERY TASKS
1) download streams and convert to images and save
2) process images and store preds (and SDI) to database
'''