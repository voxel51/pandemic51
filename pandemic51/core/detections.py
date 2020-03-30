'''
Methods for detecting objects in images.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import logging
import os
import pathlib
import random

import tensorflow as tf

import eta.core.annotations as etaa
import eta.core.image as etai
import eta.core.learning as etal

import pandemic51.config as panc
import pandemic51.core.database as pand


logger = logging.getLogger(__name__)


MODEL_NAME = "efficientdet-d4"
LABELS_WHITELIST = {"person", "bicycle", "car", "motorcycle"}
CONFIDENCE_THRESH = 0.15
ANNOTATION_CONFIG = etaa.AnnotationConfig.from_dict({
    "add_logo": False,
})


def detect_objects_in_images(inpaths, outpaths):
    '''Detects objects in the given images and writes the output labels to
    disk.

    Args:
        inpaths: a list of input paths to process
        outpaths: a list of paths to write the output labels
    '''
    detector = _load_efficientdet_model(MODEL_NAME)
    with detector:
        for inpath, outpath in zip(inpaths, outpaths):
            _process_image(detector, inpath, outpath)


def detect_objects_in_unprocessed_images():
    '''Detects objects in all images in the database that don't have labels,
    and records the object counts, ImageLabels, and annotated images for each
    of them.
    '''
    # Get the full list of unprocessed images
    unprocessed_images = pand.query_unprocessed_images()

    if not unprocessed_images:
        return

    # Process in a random order in case multiple tasks are running :)
    random.shuffle(unprocessed_images)

    detector = _load_efficientdet_model(MODEL_NAME)

    with detector:
        for id, image_path in unprocessed_images:
            ipath = pathlib.Path(image_path)

            labels_path = str(os.path.join(
                panc.LABELS_DIR, ipath.parent.stem, ipath.stem + ".json"))

            anno_path = str(os.path.join(
                panc.ANNO_DIR, ipath.parent.stem, ipath.stem + ".jpg"))

            if os.path.exists(labels_path) and os.path.exists(anno_path):
                # Another worker processed this image, so skip
                continue

            count = _process_image(
                detector, image_path, labels_path, anno_path=anno_path)

            pand.set_object_count(id, count)
            pand.add_stream_labels(id, labels_path)
            pand.add_stream_anno_img(id, anno_path)


def _load_efficientdet_model(model_name):
    tf.reset_default_graph()
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


def _filter_objects(objects):
    filters = []
    if CONFIDENCE_THRESH:
        filters.append(lambda obj: obj.confidence > CONFIDENCE_THRESH)
    if LABELS_WHITELIST:
        filters.append(lambda obj: obj.label in LABELS_WHITELIST)

    return objects.get_matches(filters, match=all)


def _process_image(detector, img_path, labels_path, anno_path=None):
    logger.info("Processing image '%s'", img_path)
    img = etai.read(img_path)

    objects = detector.detect(img)
    objects = _filter_objects(objects)

    count = len(objects)
    logger.info("Found %d objects", count)

    image_labels = etai.ImageLabels()
    image_labels.add_objects(objects)

    logger.info("Writing labels to '%s'", labels_path)
    image_labels.write_json(labels_path)

    if anno_path:
        logger.info("Writing annotated image to '%s'", anno_path)
        img_anno = etaa.annotate_image(
            img, image_labels, annotation_config=ANNOTATION_CONFIG)
        etai.write(img_anno, anno_path)

    return count
