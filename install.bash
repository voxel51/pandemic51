#!/usr/bin/env bash

# install m3u8 for streaming
git clone https://github.com/globocom/m3u8
cd m3u8
python setup.py build
python setup.py install
cd -

# install pandemic51
pip install -e .

# initialize database
p51mysql < database/init.sql
