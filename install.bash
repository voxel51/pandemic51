#!/usr/bin/env bash

# install m3u8 for streaming
git clone git@github.com:globocom/m3u8.git
cd m3u8/
python setup.py build
python setup.py install
cd -

# install submodules
git submodule update --init
pip install -r eta/requirements.txt
pip install -e eta

# install pandemic51
pip install -r requirements.txt
pip install -e .
