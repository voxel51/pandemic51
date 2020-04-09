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


image_path = \
"/scratch/jason-data/pandemic51/dublin_imgs/2020-03-16_1584359102236_1_11:45:02.jpg"
label_path = \
"/scratch/jason-data/pandemic51/dublin_labels/2020-03-16_1584359102236_1_11:45:02.json"


def lowpass(image, sigma=4.0):
    r = scipy.ndimage.gaussian_filter(image[...,0], sigma)
    g = scipy.ndimage.gaussian_filter(image[...,1], sigma)
    b = scipy.ndimage.gaussian_filter(image[...,2], sigma)
    return np.dstack((r, g, b))

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
        print(obj)
        if not obj.has_bounding_box:
            logger.debug("object without bounding box.")
            continue

        print(obj.bounding_box)

        boxtlx, boxtly = obj.bounding_box.top_left.coords_in(img=image)
        boxbrx, boxbry = obj.bounding_box.bottom_right.coords_in(img=image)
        boxw = boxbrx-boxtlx
        boxh = boxbry-boxtly

        headw = int(ceil(0.8*boxw))
        headh = int(ceil(0.16*boxh))
        headtlx = int(ceil(boxtlx+0.1*boxw))
        headtly = int(boxtly)
        headbrx = headtlx+headw
        headbry = headtly+headh

        print(boxtlx, boxtly)
        print(boxw, boxh)
        print(headtlx, headtly)
        print(headw, headh)

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

ax.imshow(image)
plt.show()


