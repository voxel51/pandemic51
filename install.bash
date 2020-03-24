#!/usr/bin/env bash

git submodule update --init

# install m3u8 for streaming
cd m3u8/
python setup.py build
python setup.py install
cd -

# install submodules
pip install -r eta/requirements.txt
pip install -e eta

# install pandemic51
pip install -r requirements.txt
pip install -e .
