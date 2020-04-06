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


def detect_objects_in_images(city, inpaths, outpaths):
    '''Detects objects in the given images and writes the output labels to
    disk.

    Args:
        inpaths: a list of input paths to process
        outpaths: a list of paths to write the output labels
    '''
    detector = _load_efficientdet_model(panc.MODEL_NAME)
    with detector:
        for inpath, outpath in zip(inpaths, outpaths):
            process_image(city, detector, inpath, outpath)


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

    detector = _load_efficientdet_model(panc.MODEL_NAME)

    with detector:
        for id, image_path, stream_name in unprocessed_images:
            ipath = pathlib.Path(image_path)

            labels_path = str(os.path.join(
                panc.LABELS_DIR, ipath.parent.stem, ipath.stem + ".json"))

            anno_path = str(os.path.join(
                panc.ANNO_DIR, ipath.parent.stem, ipath.stem + ".jpg"))

            if os.path.exists(labels_path) and os.path.exists(anno_path):
                # Another worker processed this image, so skip
                continue

            city = panc.STREAMS_MAP_INV[stream_name]
            count = process_image(
                city, detector, image_path, labels_path, anno_path=anno_path)

            pand.set_object_count(id, count)
            pand.add_stream_labels(id, labels_path)
            pand.add_stream_anno_img(id, anno_path)


def filter_objects(city, objects):
    '''Filter objects by threshold and the labels whitelist

    Args:
        city:: the city
        object: a DetectedObjectContainer

    Returns:
        a filtered DetectedObjectContainer
    '''
    filters = []
    threshold = panc.CONFIDENCE_THRESHOLDS.get(
        city, panc.DEFAULT_CONFIDENCE_THRESH)

    if threshold:
        filters.append(
            lambda obj: obj.confidence > panc.DEFAULT_CONFIDENCE_THRESH)

    if panc.LABELS_WHITELIST:
        filters.append(lambda obj: obj.label in panc.LABELS_WHITELIST)

    return objects.get_matches(filters, match=all)


def process_image(city, detector, img_path, labels_path, anno_path=None):
    '''Process an image

    Args:
        city: the city name
        detector: detector
        img_path: path to the raw image
        labels_path: the path to write the labels to
        anno_path: the path to write an anntated image to
    '''
    logger.info("Processing image '%s'", img_path)
    img = etai.read(img_path)

    objects = detector.detect(img)
    objects = filter_objects(objects)

    count = len(objects)
    logger.info("Found %d objects", count)

    image_labels = etai.ImageLabels()
    image_labels.add_objects(objects)

    logger.info("Writing labels to '%s'", labels_path)
    image_labels.write_json(labels_path)

    if anno_path:
        logger.info("Writing annotated image to '%s'", anno_path)
        img_anno = etaa.annotate_image(
            img, image_labels, annotation_config=panc.ANNOTATION_CONFIG)
        etai.write(img_anno, anno_path)

    return count


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
