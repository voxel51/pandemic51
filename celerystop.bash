#!/usr/bin/env bash
sudo systemctl stop celery.service celerybeat.service
sudo systemctl status celery.service celerybeat.service
