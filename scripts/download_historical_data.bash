#!/usr/bin/env bash
# Script for downloading historical stream data.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#


# Download images
eta gdrive download-dir 1RE-JMlKLYpQbfOkbwMFRhr_xaQ7ULVl_ data/historical/images
unzip 'data/historical/images/*.zip' -d data/historical/images
rm data/historical/images/*.zip

# Download labels
eta gdrive download-dir 1TYRgb-4JoKL8fmEqBhd5zOC3Lhs6VwOD data/historical/labels
unzip 'data/historical/labels/*.zip' -d data/historical/labels
rm data/historical/labels/*.zip
