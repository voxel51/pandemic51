#!/usr/bin/env bash

sudo apt update
sudo apt upgrade

sudo apt install git python-setuptools python-dev python-virtualenv curl rabbitmq-server
sudo apt install mysql-server mysql-client libmysqlclient-dev
sudo apt install redis-server
redis-server --daemonize yes

########### Python and PIP
pip install virtualenv

sudo mkdir $ENV_DIR

if [ -z "$ENV_DIR" ]; then
    ENV_DIR=${HOME}/venv
    export ENV_DIR
    echo "setting virtual environment directory to ${ENV_DIR}"
fi
cd ${ENV_DIR}
virtualenv -p /usr/bin/python3 covid19
cd -

# activate the `covid19` virtual environment
source ${ENV_DIR}/covid19/bin/activate
