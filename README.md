# pandemic51


Voxel51's website for monitoring the impact of the coronavirus pandemic.


## Installation


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

# virtualenv shortcuts
covid19() { source "${ENV_DIR}/covid19/bin/activate"; }
exit() {
    case `command -v python` in
        ${ENV_DIR}/*) deactivate;;
        *) builtin exit;;
    esac
}

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


### 4) Create a config

```bash
cp setup/config.py-template pandemic51/core/config.py
```

Then modify `config.py`, populating any `{{TODO}}`s with correct values. Many
of these need to exactly match the environment variable with the same name.


### 5) Initialize the database

```bash
bash init_db.bash
```

This can be run at anytime to wipe the database.


### 6) Initialize Celery

Celery is currently only configured for linux as a `systemd` daemon.

TODO(Tyler) make a configuration for Mac OS with `launchd`

1) copy the templates in `setup/` and replace any `{{ENV_VAR}}` with the
respective environment variable value.
2) Place `celery.service` & `celerybeat.service` in `/lib/systemd/system`
3) start the services:

Any time a file is added or modified in `/lib/systemd/system`
```bash
sudo systemctl daemon-reload
```

To manage the celery/beat services:
```bash
systemctl {start|stop|restart|status} celery.service celerybeat.service
```

To watch logs:
```bash
tail -f -n 10 $CELERY_DIR/worker*
```

#### 7) Download models

Download the model(s) that you need via the `download_models.py` script.


## Quickstart

Check out the following resources:

- `tests/start/`: simple tests of the initial functionality
- `tests/download_and_store/`: combines `test/start/` with DB communication
- `tests/density`: example of backend person detection on images


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
