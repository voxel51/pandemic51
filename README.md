# pandemic51
Voxel51's website for monitoring the impact of the coronavirus pandemic

## Installation:


### 1) Set Environment Variables

Put the following at the bottom of your `~/.bash_profile` or `~/.bashrc`

```bash
# Install Directory
export PANDEMIC51_BASEDIR="/pandemic51"
export ENV_DIR=${PANDEMIC51_BASEDIR}"/venv"
export DATA_DIR=${PANDEMIC51_BASEDIR}"/data"
export IMAGE_DIR=${DATA_DIR}"/images"
export LABELS_DIR=${DATA_DIR}"/labels"

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
bash install.bash
```

### 4) Initialize the database

```bash
bash init_db.bash
```

This can be run at anytime to wipe the database.

### 4) Initialize Celery

#### TODO(Tyler)


## Starting Point

Check `tests/start/` for some simple tests of the initial functionality.

`tests/download_and_store/` combines this functionality and communicates with
the database.


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
