#!/usr/bin/env bash
# Restarts the Celery service.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#

sudo systemctl restart celery.service celerybeat.service
sudo systemctl status celery.service celerybeat.service
