#!/usr/bin/env bash

sudo apt update
sudo apt upgrade

sudo snap install ffmpeg

sudo apt install git python-setuptools python-dev python-virtualenv curl rabbitmq-server
sudo apt install mysql-server mysql-client libmysqlclient-dev
sudo apt install redis-server
redis-server --daemonize yes

########### Python and PIP
#
# Install Python 3.6, pip, and virtualenv
#
# Makes `python` and `pip` point to Python 3, which is required by pandemic51
#
# These instructions assume you are using Ubuntu 16.04, which does not come
# with Python 3.6 by default. More recent versions of Ubuntu may have
# Python 3.6 installed by default
echo "--- INSTALLING PYTHON 3.6 ---"
sudo apt-get -y --no-install-recommends install software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get -y --no-install-recommends install python3.6 python3.6-dev
sudo ln -s /usr/bin/python3.6 /usr/local/bin/python
curl https://bootstrap.pypa.io/get-pip.py | sudo python
sudo pip install --upgrade pip setuptools
sudo pip install virtualenv

mkdir -p $ENV_DIR

if [ -z "$ENV_DIR" ]; then
    ENV_DIR=${HOME}/venv
    export ENV_DIR
    echo "setting virtual environment directory to ${ENV_DIR}"
fi
cd ${ENV_DIR}
virtualenv -p /usr/bin/python3.6 covid19
cd -

########### Celery
mkdir -p $CELERY_DIR

sudo chown -R www-data $CELERY_DIR
