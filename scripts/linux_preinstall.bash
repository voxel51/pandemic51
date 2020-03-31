#!/usr/bin/env bash
# Linux preinstall script.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#

sudo apt update
sudo apt upgrade

sudo apt install unzip
sudo apt install git python-setuptools python-dev python-virtualenv curl rabbitmq-server
sudo apt install mysql-server mysql-client libmysqlclient-dev
sudo apt install redis-server
sudo apt-get install chrome-browser
redis-server --daemonize yes

#
# Install Python 3.6, pip, and virtualenv
#
# Makes `python` and `pip` point to Python 3, which is required by pandemic51
#
# These instructions assume you are using Ubuntu 16.04, which does not come
# with Python 3.6 by default. More recent versions of Ubuntu may have
# Python 3.6 installed by default
#
sudo apt-get -y --no-install-recommends install software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get -y --no-install-recommends install python3.6 python3.6-dev
sudo ln -s /usr/bin/python3.6 /usr/local/bin/python
curl https://bootstrap.pypa.io/get-pip.py | sudo python
sudo pip install --upgrade pip setuptools
sudo pip install virtualenv

# Initialize directories
mkdir -p "${P51_CELERY_DIR}"
mkdir -p "${P51_DATA_DIR}/images"
mkdir -p "${P51_DATA_DIR}/labels"
mkdir -p "${P51_DATA_DIR}/anno"
