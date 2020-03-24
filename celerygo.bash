#!/usr/bin/env bash
sudo systemctl restart celery.service celerybeat.service
sudo systemctl status celery.service celerybeat.service

