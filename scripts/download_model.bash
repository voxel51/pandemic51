#!/usr/bin/env bash
# Script for downloading the detection model checkpoint.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#

#
# EfficientDet-D4 checkpoint
# Original source: https://github.com/google/automl/tree/master/efficientdet
#
eta gdrive download --public 1h4zTgbQJdpkJodvi0RiXLyQ_tPp3zTWl models/efficientdet-d4.tar.gz
tar -xf models/efficientdet-d4.tar.gz -C models/
rm models/efficientdet-d4.tar.gz
