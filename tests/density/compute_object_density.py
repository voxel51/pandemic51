'''
Test script demonstrating object density calculation on a set of images.

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

import eta.core.annotations as etaa
import eta.core.image as etai
import eta.core.utils as etau

import pandemic51.core.density as pand


IMAGES_DIR = "data/prague_imgs"
#IMAGES_DIR = "data/timessquare_imgs"
LABELS_DIR = "out/labels"
IMAGES_ANNO_DIR = "out/anno"


# Input images to process
#inpaths = etau.list_files(IMAGES_DIR, abs_paths=True)[:10]
inpaths = etau.list_files(IMAGES_DIR, abs_paths=True)

# Path to write output labels
outpaths = [
    os.path.join(
        LABELS_DIR, os.path.splitext(os.path.basename(inpath))[0] + ".json")
    for inpath in inpaths]

# Compute object density
pand.compute_object_density_for_images(inpaths, outpaths)

# Render output annotations
config = etaa.AnnotationConfig.from_dict({
    "add_logo": False,
    "show_all_confidences": True,
})
for inpath, outpath in zip(inpaths, outpaths):
    annopath = os.path.join(IMAGES_ANNO_DIR, os.path.basename(inpath))

    img = etai.read(inpath)
    image_labels = etai.ImageLabels.from_json(outpath)
    img_anno = etaa.annotate_image(img, image_labels, annotation_config=config)
    etai.write(img_anno, annopath)
