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
from math import ceil

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import scipy.ndimage

import pandemic51.core.detections as pand
import eta.core.annotations as etaa
import eta.core.image as etai
import eta.core.objects as etao

logger = logging.getLogger(__name__)


def lowpass(image, sigma=3.0):
    r = scipy.ndimage.gaussian_filter(image[...,0], sigma)
    g = scipy.ndimage.gaussian_filter(image[...,1], sigma)
    b = scipy.ndimage.gaussian_filter(image[...,2], sigma)
    return np.dstack((r, g, b))

def redact(image_path, label_path):
    image = etai.to_float(etai.read(image_path))
    gauss = lowpass(image)
    labels = etai.ImageLabels.from_json(label_path)

    schema_filter = etao.ObjectContainerSchema()
    schema_filter.add_object_label("person")

    fig, ax = plt.subplots(1)

    if labels.has_objects:
        labels.objects.filter_by_schema(schema_filter)
        logger.debug("Rendering %d objects", len(labels.objects))
        for obj in labels.objects:
            if not obj.has_bounding_box:
                logger.debug("object without bounding box.")
                continue

            boxtlx, boxtly = obj.bounding_box.top_left.coords_in(img=image)
            boxbrx, boxbry = obj.bounding_box.bottom_right.coords_in(img=image)
            boxw = boxbrx-boxtlx
            boxh = boxbry-boxtly

            headw = int(ceil(0.6*boxw))
            headh = int(ceil(0.16*boxh))
            headtlx = int(ceil(boxtlx+0.2*boxw))
            headtly = int(boxtly)
            headbrx = headtlx+headw
            headbry = headtly+headh

            box = pat.Rectangle((boxtlx, boxtly), boxw, boxh,
                                linewidth=0.25,
                                edgecolor='r',
                                facecolor='none')
            ax.add_patch(box)

            head = pat.Rectangle((headtlx, headtly), headw, headh,
                                 linewidth=0.5,
                                 edgecolor='b',
                                 facecolor='none')

            ax.add_patch(head)

            image[headtly:headbry, headtlx:headbrx, :] = \
                    gauss[headtly:headbry, headtlx:headbrx, :]

    etai.write(image*255, "/tmp/redacted.jpg")

    ax.imshow(image)
    plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="test_redaction.py", add_help=True)
    parser.add_argument("image_path", help="path to the source image")
    parser.add_argument("label_path", help="path to the labels on the source")
    args = parser.parse_args()

    redact(args.image_path, args.label_path)


