#!/usr/bin/env bash
# Stops the Celery service.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#

sudo systemctl stop celery.service celerybeat.service
sudo systemctl status celery.service celerybeat.service
