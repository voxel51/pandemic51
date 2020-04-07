'''
Script for computing object counts for a set of images.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import os

import eta.core.annotations as etaa
import eta.core.image as etai
import eta.core.utils as etau

import pandemic51.config as panc
import pandemic51.core.detections as pand


IMAGES_DIR = os.path.join(
    panc.PANDEMIC51_DIR, "data/historical/images/timessquare_imgs")

LABELS_DIR = "out/labels"
IMAGES_ANNO_DIR = "out/anno"

ANNOTATION_CONFIG = etaa.AnnotationConfig.from_dict({
    "add_logo": False,
    "show_all_confidences": True,
})


# Input images to process
inpaths = etau.list_files(IMAGES_DIR, abs_paths=True)  # all
#inpaths = etau.list_files(IMAGES_DIR, abs_paths=True)[:50]  # first 50

# Path to write output labels
outpaths = [
    os.path.join(
        LABELS_DIR, os.path.splitext(os.path.basename(inpath))[0] + ".json")
    for inpath in inpaths]

# Detect objects in images
pand.detect_objects_in_images("newyork", inpaths, outpaths)

# Render output annotations
for inpath, outpath in zip(inpaths, outpaths):
    annopath = os.path.join(IMAGES_ANNO_DIR, os.path.basename(inpath))

    img = etai.read(inpath)
    image_labels = etai.ImageLabels.from_json(outpath)
    img_anno = etaa.annotate_image(
        img, image_labels, annotation_config=ANNOTATION_CONFIG)
    etai.write(img_anno, annopath)
