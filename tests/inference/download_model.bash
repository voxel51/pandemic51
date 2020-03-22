#!/bin/bash
# Download a detection model and labels
#
# Usage:
#   bash download_model.bash
#
# Copyright 2017-2020, Voxel51, Inc.
# Tyler Ganter, tyler@voxel51.com
#
MODEL_NAME=coco_ssd_mobilenet_v1_1.0_quant_2018_06_29

wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/${MODEL_NAME}.zip

unzip ${MODEL_NAME}.zip -d model/

rm ${MODEL_NAME}.zip