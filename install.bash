#!/usr/bin/env bash

git submodule update --init

# install m3u8 for streaming
python m3u8/setup.py build
python m3u8/setup.py install

# install submodules
pip install -r eta/requirements.txt
pip install -e eta

# install pandemic51
pip install -r requirements.txt
pip install -e .
