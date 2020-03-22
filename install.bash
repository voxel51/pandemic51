#!/usr/bin/env bash

# install m3u8 for streaming
git clone https://github.com/globocom/m3u8
cd m3u8
python setup.py build
python setup.py install
cd -

# install submodules
pip install -r eta/requirements.txt
pip install -e eta

# install pandemic51
pip install -e .
pip install -r requirements.txt
