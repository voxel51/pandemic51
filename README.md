# pandemic51
Voxel51's website for monitoring the impact of the coronavirus pandemic

## Installation:


### 1) Set Environment Variables

Put the following at the bottom of your `~/.bash_profile` or `~/.bashrc`

```bash
# Resource Directories
export P51_BASEDIR="/home/<USER>/p51_base"
export ENV_DIR=${P51_BASEDIR}"/venv"
export CELERY_DIR=${P51_BASEDIR}"/celery"
export DATA_DIR=${P51_BASEDIR}"/data"
export IMAGE_DIR=${DATA_DIR}"/images"
export LABELS_DIR=${DATA_DIR}"/labels"

# Repository Directory
export P51_REPO_DIR="<PANDEMIC51/PARENT/DIR>"

# MySQL
export P51_SQL_USERNAME="<USERNAME>"
export P51_SQL_PASSWORD="<PASSWORD>"
export P51_SQL_DATABASE_NAME="p51db"

# login shortcut command
alias p51mysql="mysql -u $P51_SQL_USERNAME -p$P51_SQL_PASSWORD $P51_SQL_DATABASE_NAME"
```

### 2) Pre-installation
Before running the installation script, following the instructions in
`mac_preinstall.md` for Mac local development or run `linux_preinstall.bash`
for linux systems.


### 3) Install
```bash
# activate the `covid19` virtual environment
source ${ENV_DIR}/covid19/bin/activate

bash install.bash
```

### 4) Initialize the database

```bash
bash init_db.bash
```

This can be run at anytime to wipe the database.

### 5) Initialize Celery

1) copy the templates in `setup/` and replace any `{{ENV_VAR}}` with the
respective environment variable value.
2) Place `celery.service` in `/lib/systemd/system`
3) 

```bash
sudo systemctl daemon-reload
sudo systemctl start celery.service


sudo systemctl restart celery.service

sudo systemctl restart celery.service celerybeat.service
```


## Starting Point

Check `tests/start/` for some simple tests of the initial functionality.

`tests/download_and_store/` combines this functionality and communicates with
the database.


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
