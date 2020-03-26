'''Add Historical Data to the database and data store

Copyright 2017-2020, Voxel51, Inc.
voxel51.com

Tyler Ganter, tyler@voxel51.com
'''
from datetime import datetime
import logging
import os
import pathlib
import shutil

import pandemic51.core.config as panc
import pandemic51.core.database as pand
import pandemic51.core.utils as panu


logger = logging.getLogger(__name__)


dir_path = os.path.dirname(os.path.realpath(__file__))
historical_dir = pathlib.Path(dir_path).parent.parent.joinpath(
    "data", "historical")

images_dir = os.path.join(historical_dir, "images")
labels_dir = os.path.join(historical_dir, "labels")

stream_name_map = {
    "timessquare": "time_square"
}

for cur_images_dir, _, files in os.walk(images_dir):
    if not files:
        continue

    stream_dirname = pathlib.Path(cur_images_dir).stem[:-len("_imgs")]
    cur_labels_dir = os.path.join(labels_dir, stream_dirname + "_labels")

    stream_name = (
        stream_name_map[stream_dirname]
        if stream_dirname in stream_name_map else stream_dirname
    )

    assert stream_name in panc.STREAMS, \
        "Unknown stream_name: '{}'".format(stream_name)

    for filename in files:
        json_filename = os.path.splitext(filename)[0] + ".json"

        img_path = os.path.join(cur_images_dir, filename)
        labels_path = os.path.join(cur_labels_dir, json_filename)

        # UTC time
        timestamp = panu.parse_epoch_timestamp_from_path(img_path)
        utc_dt = datetime.utcfromtimestamp(timestamp)

        new_img_path = os.path.join(panc.IMAGE_DIR, stream_name, filename)
        new_labels_path = os.path.join(
            panc.LABELS_DIR, stream_name, json_filename)

        assert os.path.exists(img_path), "Missing image: %s" % img_path
        assert os.path.exists(labels_path), "Missing labels: %s" % labels_path

        logger.info("Moving file:\n\t%s\n\t-> %s" % (img_path, new_img_path))
        shutil.move(img_path, new_img_path)

        logger.info("Moving file:\n\t%s\n\t-> %s" % (labels_path, new_labels_path))
        shutil.move(labels_path, new_labels_path)

        logger.info("Adding stream history:\n\t%s | %s | %s | %s"
                    % (stream_name, utc_dt, new_img_path, new_labels_path))
        pand.add_stream_history(
            stream_name, utc_dt,
            image_path=new_img_path,
            labels_path=new_labels_path
        )
