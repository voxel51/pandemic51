'''
Convert a video to a configurable-resolution image

'''
import glob
import os
import sys

import ffmpy

sys.path.append(sys.path.append(os.path.realpath(__file__)))
from download_stream import ensure_dir


def vid2img(inpath, outpath, width=300, height=300):
    if os.path.exists(outpath):
        return False

    ensure_dir(outpath)

    outcmd = "-ss 00:00:00 -t 00:00:01 -s %dx%d -r 1 -f image2" \
             % (width, height)

    cmd = ffmpy.FFmpeg(
        inputs={inpath:None },
        outputs={outpath: outcmd}
    )

    if not os.path.exists(outpath):
        cmd.run()

    return True


if __name__ == '__main__':
    input_pattern = "out/time_square/*.mp4"
    out_dir = "out/time_square_img"

    for input_path in glob.glob(input_pattern):
        print(input_path)

        outfilename = os.path.splitext(os.path.basename(input_path))[0] + ".png"
        out_path = os.path.join(out_dir, outfilename)

        vid2img(input_path, out_path)
