#!/usr/bin/env bash
# Installs pandemic51 and its dependencies.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#


# Initialize submodules
git submodule init
git submodule update


# Install m3u8
echo "***** INSTALLING M3U8 *****"
if [[ ! -d m3u8 ]]; then
    git clone https://github.com/globocom/m3u8
fi
cd m3u8
python setup.py build
python setup.py install
cd -


# Install ETA
echo "***** INSTALLING ETA *****"
cd eta
bash install.bash
if [[ ! -f config.json ]]; then
    cp config-example.json config.json
fi
cd ..


# Install pandemic51
echo "***** INSTALLING PANDEMIC51 *****"
pip install -e .
pip install -r requirements.txt


# Install COCO API (required by `automl/efficientdet`)
echo "***** INSTALLING COCO API *****"
git clone https://github.com/cocodataset/cocoapi.git
make --directory=cocoapi/PythonAPI
cp -r cocoapi/PythonAPI/pycocotools eta/tensorflow/models/research/
rm -rf cocoapi
