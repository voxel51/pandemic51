'''
Methods for detecting objects in images.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import logging
import os
import pathlib
import random
from math import ceil

import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np
import scipy.ndimage
import tensorflow as tf

import eta.core.annotations as etaa
import eta.core.geometry as etag
import eta.core.image as etai
import eta.core.learning as etal

import pandemic51.config as panc
import pandemic51.core.database as pand

logger = logging.getLogger(__name__)


def detect_objects_in_images(city, inpaths, outpaths):
    '''Detects objects in the given images and writes the output labels to
    disk.

    Args:
        city: the city
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
            try:
                city = panc.STREAMS_MAP_INV[stream_name]
            except:
                continue
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
            lambda obj: obj.confidence > threshold)

    if panc.LABELS_WHITELIST:
        filters.append(lambda obj: obj.label in panc.LABELS_WHITELIST)

    return objects.get_matches(filters, match=all)


def process_image(city, detector, img_path, labels_path, anno_path=None):
    '''Process an image

    Args:
        city: the city
        detector: detector
        img_path: the path to the raw image
        labels_path: the path to write the labels to
        anno_path: the path to write an anntated image to
    '''
    logger.info("Processing image '%s'", img_path)
    img = etai.read(img_path)

    raw_objects = detector.detect(img)
    objects = filter_objects(city, raw_objects)

    count = len(objects)
    logger.info("Found %d objects", count)

    raw_image_labels = etai.ImageLabels()
    raw_image_labels.add_objects(raw_objects)

    logger.info("Writing labels to '%s'", labels_path)
    raw_image_labels.write_json(labels_path)

    if anno_path:
        img = redact(img, objects)
        _annotate_img(img, objects, anno_path)

    return count


def redact(image, objects, visualize=False):
    '''Redact the faces of the detected people in the image.

    Only detections with label "person" are used, but the detections may have
    other objects as well.

    Args:
        image: numpy image
        objects: DetectedObjectContainer
        visualize: boolean (False) to interactively plot the redaction data

    Returns:
        the redacted image with no boxes overlayed on it
    '''
    gauss = _lowpass(image)

    for obj in objects:
        if obj.label != "person":
            continue

        if not obj.has_bounding_box:
            logger.debug("object without bounding box.")
            continue

        headbox = _headbox(obj.bounding_box, image)
        headtlx, headtly = headbox.top_left.coords_in(img=image)
        headbrx, headbry = headbox.bottom_right.coords_in(img=image)

        image[headtly:headbry, headtlx:headbrx, :] = \
            gauss[headtly:headbry, headtlx:headbrx, :]

    if visualize:
        _, ax = plt.subplots(1)
        for obj in objects:
            if obj.label != "person":
                continue

            if not obj.has_bounding_box:
                continue

            boxtlx, boxtly = obj.bounding_box.top_left.coords_in(img=image)
            boxbrx, boxbry = \
                obj.bounding_box.bottom_right.coords_in(img=image)
            boxw = boxbrx-boxtlx
            boxh = boxbry-boxtly

            headbox = _headbox(obj.bounding_box, image)
            headtlx, headtly = headbox.top_left.coords_in(img=image)
            headbrx, headbry = headbox.bottom_right.coords_in(img=image)
            headw = int(ceil(headbrx-headtlx))
            headh = int(ceil(headbry-headtly))

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

    return image


def update(city, img_path, labels_path, anno_path=None):
    '''Loads the raw labels, filters down the objects based on the (new)
    threshold, and optionally updates the annotated image.

    Args:
        city: the city name
        detector: detector
        img_path: the path to the raw image
        labels_path: the path to write the labels to
        anno_path: the path to write an anntated image to
    '''
    raw_image_labels = etai.ImageLabels.from_json(labels_path)
    logger.info("Loaded %d raw objects", len(raw_image_labels.objects))

    objects = filter_objects(city, raw_image_labels.objects)
    new_count = len(objects)
    logger.info("Filtered down to %d objects", new_count)

    if anno_path:
        img = redact(etai.read(img_path), objects)
        _annotate_img(img, objects, anno_path)

    return new_count


def _annotate_img(img, objects, anno_path):
    image_labels = etai.ImageLabels()
    image_labels.add_objects(objects)
    logger.info("Writing annotated image to '%s'", anno_path)
    img_anno = etaa.annotate_image(
        img, image_labels, annotation_config=panc.ANNOTATION_CONFIG)
    etai.write(img_anno, anno_path)


def _headbox(box, image):
    '''Convert the person bounding box to a smaller one with relative size for
    identifying the head region of the person.

    Args:
        box: etag.BoundingBox relative bounding box (to image)
        image: ndarray containing the image, used for sizing

    All processing happens in relative coords.

    The method establishes a rectangular region as a function of the object
    bounding box.  Because the content of the box is expected to vary based on
    the aspect ratio (if we only get head and shoulders, then we have a
    square-shaped box), we vary the shape of this head region as a function of
    the aspect ratio.  This is not a general method, do not use elsewhere.
    '''
    # constants derived from data samples
    tallbox = (0.7, 0.18)
    tallar = 0.35
    shortbox = (0.7, 0.56)
    shortar = 1.1

    # assumes the width is the same, and tallbox is less than shortbox
    r_o = tallar
    r_t = shortar-tallar
    s_o = tallbox[1]
    s_t = shortbox[1]-tallbox[1]

    x = box.aspect_ratio_in(img=image)
    xhat = (x - r_o) / r_t
    size = (tallbox[0], s_o + xhat * s_t)

    boxtlx, boxtly = box.top_left.to_tuple()
    boxbrx, boxbry = box.bottom_right.to_tuple()
    boxw = boxbrx-boxtlx
    boxh = boxbry-boxtly

    headw = size[0]*boxw
    headh = size[1]*boxh
    headtlx = boxtlx+((1.0-size[0])/2)*boxw
    headtly = boxtly
    headbrx = headtlx+headw
    headbry = headtly+headh

    return etag.BoundingBox.from_coords(headtlx, headtly, headbrx, headbry)


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


def _lowpass(image, sigma=3.0):
    '''Perform a simple lowpass filter on the image to smooth and hide its
    detail content.
    '''
    r = scipy.ndimage.gaussian_filter(image[..., 0], sigma)
    g = scipy.ndimage.gaussian_filter(image[..., 1], sigma)
    b = scipy.ndimage.gaussian_filter(image[..., 2], sigma)
    return np.dstack((r, g, b))
