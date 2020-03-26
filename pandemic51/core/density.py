'''
Computes object density in a collection of images.

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

import os
import logging

import numpy as np

import eta.core.data as etad
import eta.core.image as etai
import eta.core.learning as etal
import eta.core.utils as etau

import pandemic51.constants as panc


logger = logging.getLogger(__name__)


#MODEL_NAME = "efficientdet-d0"
MODEL_NAME = "efficientdet-d4"
#MODEL_NAME = "efficientdet-d6"

LABELS_WHITELIST = {"person", "bicycle", "car", "motorcycle"}

CONFIDENCE_THRESH = 0
#CONFIDENCE_THRESH = 0.15


def load_efficientdet_model(model_name):
    config = etal.ModelConfig.from_dict(
        {
            "type": "pandemic51.detectors.EfficientDet",
            "config": {
                "model_path": os.path.join(panc.MODELS_DIR, model_name),
                "architecture_name": model_name,
                "labels_path": "{{eta-resources}}/ms-coco-labels.txt",
            }
        })
    return config.build()


def compute_object_density(objects):
    # @todo could implement a proper scanline algorithm for this
    mask = np.zeros((512, 512), dtype=bool)
    for obj in objects:
        tlx, tly, w, h = obj.bounding_box.coords_in(img=mask)
        mask[tly:tly + h, tlx:tlx + w] = True

    return mask.sum() / mask.size


def filter_objects(objects):
    filters = []
    if CONFIDENCE_THRESH:
        filters.append(lambda obj: obj.confidence > CONFIDENCE_THRESH)
    if LABELS_WHITELIST:
        filters.append(lambda obj: obj.label in LABELS_WHITELIST)

    return objects.get_matches(filters, match=all)


def compute_object_density_for_images(inpaths, outpaths):
    detector = load_efficientdet_model(MODEL_NAME)

    with detector:
        for inpath, outpath in zip(inpaths, outpaths):
            logger.info("Processing image '%s'", inpath)
            img = etai.read(inpath)

            objects = detector.detect(img)
            objects = filter_objects(objects)

            count = len(objects)
            density = compute_object_density(objects)
            logger.info("Found %d objects (density = %.3f)", count, density)

            image_labels = etai.ImageLabels()
            image_labels.add_objects(objects)
            image_labels.add_attribute(
                etad.NumericAttribute("count", count))
            image_labels.add_attribute(
                etad.NumericAttribute("density", density))

            logger.info("Writing labels to '%s'", outpath)
            image_labels.write_json(outpath)
