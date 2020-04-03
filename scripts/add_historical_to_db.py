'''
Adds historical data to the database and data store.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from datetime import datetime
import logging
import os
import pathlib

import eta.core.utils as etau

import pandemic51.config as panc
import pandemic51.core.database as pand
import pandemic51.core.utils as panu


logger = logging.getLogger(__name__)


historical_dir = os.path.join(panc.PANDEMIC51_DIR, "data", "historical")
images_dir = os.path.join(historical_dir, "images")

streams_map = {
    "timessquare": "time_square"
}

for cur_images_dir, _, files in os.walk(images_dir):
    if not files:
        continue

    stream_dirname = pathlib.Path(cur_images_dir).stem[:-len("_imgs")]

    stream_name = (
        streams_map[stream_dirname]
        if stream_dirname in streams_map else stream_dirname
    )

    assert stream_name in panc.STREAMS, \
        "Unknown stream_name: '{}'".format(stream_name)

    for filename in files:
        json_filename = os.path.splitext(filename)[0] + ".json"

        img_path = os.path.join(cur_images_dir, filename)

        # UTC time
        timestamp = panu.parse_epoch_timestamp_from_path(img_path)
        utc_dt = datetime.utcfromtimestamp(timestamp)

        new_img_path = os.path.join(panc.IMAGES_DIR, stream_name, filename)

        assert os.path.exists(img_path), "Missing image: %s" % img_path

        logger.info("Moving file:\n\t%s\n\t-> %s", img_path, new_img_path)
        etau.move_file(img_path, new_img_path)

        logger.info("Adding stream history:\n\t%s | %s | %s",
                    stream_name, utc_dt, new_img_path)
        pand.add_stream_history(stream_name, utc_dt, image_path=new_img_path)
