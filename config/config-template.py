'''
Backend app config.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
import os

import eta.core.annotations as etaa


###############################################################################
# MySQL
###############################################################################

#
# If running locally, use the TCP connections
#
# Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy) so that
# your application can use 127.0.0.1:3306 to connect to your Cloud SQL instance
#
SQL_HOST = "127.0.0.1"

# MySQL
P51_SQL_USERNAME = "{{P51_SQL_USERNAME}}"
P51_SQL_PASSWORD = "{{P51_SQL_PASSWORD}}"
P51_SQL_DATABASE_NAME = "p51db"

###############################################################################
# API
###############################################################################

BASE_API_URL = "https://pdi-service.voxel51.com"
SNAPSHOTS_URL = BASE_API_URL + "/snapshots"

###############################################################################
# Resource directories
###############################################################################

# cloned repo
PANDEMIC51_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(PANDEMIC51_DIR)  # directory above repo clone
CONFIG_DIR = os.path.join(PANDEMIC51_DIR, "config")
MODELS_DIR = os.path.join(PANDEMIC51_DIR, "models")
EFFICIENTDET_DIR = os.path.join(PANDEMIC51_DIR, "automl", "efficientdet")

DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
LABELS_DIR = os.path.join(DATA_DIR, "labels")
ANNO_DIR = os.path.join(DATA_DIR, "anno")

###############################################################################
# Streams
###############################################################################

STREAMS_DIR = os.path.join(CONFIG_DIR, "streams")
STREAMS_MAP = {  # maps city names to stream names
    "london": "abbey_road",
    "chicago": "chicago",
    "dublin": "dublin",
    "newjersey": "new_jersey",
    "prague": "prague",
    "newyork": "time_square",
    "neworleans": "new_orleans",
}
STREAMS_MAP_INV = {v: k for k, v in STREAMS_MAP.items()}

# names of US cities
US_CITIES = {"chicago", "newyork", "neworleans", "newjersey"}
# streams to be omitted from average
BETA_STREAMS = {"detroit", "annarbor", "ypsilanti"}

###############################################################################
# DETECTOR
###############################################################################

MODEL_NAME = "efficientdet-d4"
LABELS_WHITELIST = {"person", "bicycle", "car", "motorcycle"}


DEFAULT_CONFIDENCE_THRESH = 0.15

CONFIDENCE_THRESHOLDS = {
    "<city>": 0.5,
}

ANNOTATION_CONFIG = etaa.AnnotationConfig.from_dict({
    "add_logo": False,
})

###############################################################################
# Events
###############################################################################

EVENTS_PATH = os.path.join(CONFIG_DIR, "news_events.csv")

###############################################################################
# Celery
###############################################################################

DOWNLOAD_STREAM_INTERVAL = 60 * 15
COMPUTE_DETECTIONS_INTERVAL = 60 * 15
