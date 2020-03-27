'''
pandemic51 config.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
import os

import eta.core.serial as etas

#
# If running locally, use the TCP connections
#
# Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
# so that your application can use 127.0.0.1:3306 to connect to your
# Cloud SQL instance
#
SQL_HOST = "127.0.0.1"

# Resource directories
P51_BASEDIR = "/home/{{USER}}/p51_base" # TODO REPLACE ME
ENV_DIR = os.path.join(P51_BASEDIR, "venv")
CELERY_DIR = os.path.join(P51_BASEDIR, "celery")
DATA_DIR = os.path.join(P51_BASEDIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
LABELS_DIR = os.path.join(DATA_DIR, "labels")
ANNO_DIR = os.path.join(DATA_DIR, "anno")

# Repository directory
P51_REPO_DIR = "{{PANDEMIC51/PARENT/DIR}}" # TODO REPLACE ME

# MySQL
P51_SQL_USERNAME = "{{USERNAME}}" # TODO REPLACE ME
P51_SQL_PASSWORD = "{{PASSWORD}}" # TODO REPLACE ME
P51_SQL_DATABASE_NAME = "p51db"

# Stream info
STREAMS_PATH = os.path.join(P51_REPO_DIR, "pandemic51/config/streams.json")
STREAMS = etas.load_json(STREAMS_PATH)

# Celery periodic task intervals
DOWNLOAD_STREAM_INTERVAL = 60 * 15
COMPUTE_DETECTIONS_INTERVAL = 60 * 15
