#!/usr/bin/env bash
# Script for downloading historical stream data.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#

eta gdrive download --public 1zxzxBz0DyKvETMUvB2tTlVZd4b4kPttB data/historical.tar.gz
tar -xf data/historical.tar.gz -C data/
rm data/historical.tar.gz
