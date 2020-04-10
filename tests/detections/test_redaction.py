'''
Test that we can redact the faces in

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
# pragma pylint: disable=redefined-builtin
# pragma pylint: disable=unused-wildcard-import
# pragma pylint: disable=wildcard-import
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import *
# pragma pylint: enable=redefined-builtin
# pragma pylint: enable=unused-wildcard-import
# pragma pylint: enable=wildcard-import

import argparse
import logging

import numpy as np

import pandemic51.core.detections as pand
import eta.core.image as etai

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="test_redaction.py", add_help=True)
    parser.add_argument("image_path", help="path to the source image")
    parser.add_argument("label_path", help="path to the labels on the source")
    parser.add_argument("--output", "-o", default=None,
                        help="path to write the redacted image")

    parser.add_argument("-v", dest="visualize", action="store_true")
    parser.add_argument("--visualize", dest="visualize",
                        action="store_true")
    parser.add_argument("--no-visualize", dest="visualize",
                        action="store_false")
    parser.set_defaults(visualize=False)

    parser.add_argument("-d", "--dual", nargs="?", default=None,
        help="generate a dual view for debugging, provide path for the output")


    args = parser.parse_args()

    image = etai.read(args.image_path)
    labels = etai.ImageLabels.from_json(args.label_path)
    redacted = pand.redact(image, labels.objects, visualize=args.visualize)

    if args.output:
        etai.write(redacted, args.output)

    if args.dual:
        source = etai.read(args.image_path)
        h, w, b = image.shape
        dual = np.zeros((h*2, w, b), dtype=np.uint8)
        dual[0:h, ...] = source[0:h, ...]
        dual[h:2*h, ...] = redacted[0:h, ...]

        etai.write(dual, args.dual)

