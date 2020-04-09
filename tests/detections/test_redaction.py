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

def redact(image_path, label_path, size=(0.6, 0.16), visualize=False):
    '''Redact the faces of the detected people in the image.

    Only detections with label "person" are used, but the detections may have
    other objects as well.

    Args:
        image_path: string describing the location of the image
        label_path: string description the location of the serialized
            ImageLabels json containing the detections
        size: tuple for width, height representation in [0, 1] to use as the
            size of the face to redact
        visualize: boolean (False) to interactively plot the redaction data

    Returns:
        the redacted image with no boxes overlayed on it
    '''

    image = etai.to_float(etai.read(image_path))
    gauss = lowpass(image)
    labels = etai.ImageLabels.from_json(label_path)

    schema_filter = etao.ObjectContainerSchema()
    schema_filter.add_object_label("person")

    if labels.has_objects:
        labels.objects.filter_by_schema(schema_filter)
        for obj in labels.objects:
            if not obj.has_bounding_box:
                logger.debug("object without bounding box.")
                continue

            boxtlx, boxtly = obj.bounding_box.top_left.coords_in(img=image)
            boxbrx, boxbry = obj.bounding_box.bottom_right.coords_in(img=image)
            boxw = boxbrx-boxtlx
            boxh = boxbry-boxtly

            headw = int(ceil(size[0]*boxw))
            headh = int(ceil(size[1]*boxh))
            headtlx = int(ceil(boxtlx+((1.0-size[0])/2)*boxw))
            headtly = int(boxtly)
            headbrx = headtlx+headw
            headbry = headtly+headh

            image[headtly:headbry, headtlx:headbrx, :] = \
                    gauss[headtly:headbry, headtlx:headbrx, :]


    if visualize:
        fig, ax = plt.subplots(1)
        if labels.has_objects:
            labels.objects.filter_by_schema(schema_filter)
            for obj in labels.objects:
                if not obj.has_bounding_box:
                    continue

                boxtlx, boxtly = obj.bounding_box.top_left.coords_in(img=image)
                boxbrx, boxbry = obj.bounding_box.bottom_right.coords_in(img=image)
                boxw = boxbrx-boxtlx
                boxh = boxbry-boxtly

                headw = int(ceil(size[0]*boxw))
                headh = int(ceil(size[1]*boxh))
                headtlx = int(ceil(boxtlx+((1.0-size[0])/2)*boxw))
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

        ax.imshow(image)
        plt.show()

    return image*255

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="test_redaction.py", add_help=True)
    parser.add_argument("image_path", help="path to the source image")
    parser.add_argument("label_path", help="path to the labels on the source")

    parser.add_argument("-v", dest="visualize", action="store_true")
    parser.add_argument("--visualize", dest="visualize",
                        action="store_true")
    parser.add_argument("--no-visualize", dest="visualize",
                        action="store_false")
    parser.set_defaults(visualize=False)
    args = parser.parse_args()

    redacted = redact(args.image_path, args.label_path, visualize=args.visualize)

    etai.write(redacted, "/tmp/redacted.jpg")
