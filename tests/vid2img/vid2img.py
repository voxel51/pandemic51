'''
Convert a video to a configurable-resolution image

'''
import glob
import os

from pandemic51.core.vid2img import vid2img

input_pattern = "../out/video/time_square/*.mp4"
out_dir = "../out/img/time_square"

for input_path in glob.glob(input_pattern):
    outfilename = os.path.splitext(os.path.basename(input_path))[0] + ".png"
    out_path = os.path.join(out_dir, outfilename)

    vid2img(input_path, out_path)
