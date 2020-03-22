'''
Convert a video to a configurable-resolution image

'''
import os

import ffmpy

import eta.core.utils as etau


def vid2img(inpath, outpath, width=300, height=300):
    if os.path.exists(outpath):
        return False

    etau.ensure_basedir(outpath)

    outcmd = "-ss 00:00:00 -t 00:00:01 -s %dx%d -r 1 -f image2" \
             % (width, height)

    cmd = ffmpy.FFmpeg(
        inputs={inpath:None },
        outputs={outpath: outcmd}
    )

    if not os.path.exists(outpath):
        cmd.run()

    return True
