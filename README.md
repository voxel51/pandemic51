# pandemic51

Voxel51's website for monitoring the impact of the Coronavirus pandemic.
See it live at https://pdi.voxel51.com.

<img src="https://user-images.githubusercontent.com/3719547/74191434-8fe4f500-4c21-11ea-8d73-555edfce0854.png" alt="voxel51-logo.png" width="40%"/>


## Organization

```
.
├── api                      <-- backend API
├── config                   <-- config files and templates
├── pandemic51               <-- core backend libary
├── README.md                <-- this README
└── web                      <-- web client
```


## Installation

### Environment variables and configuration

Add the following to your `~/.bash_profile` or `~/.bashrc`:

```bash
# Resource Directories
export P51_BASEDIR="/home/<USER>/p51_base"
export ENV_DIR=${P51_BASEDIR}"/venv"
export CELERY_DIR=${P51_BASEDIR}"/celery"
export DATA_DIR=${P51_BASEDIR}"/data"
export IMAGE_DIR=${DATA_DIR}"/images"
export LABELS_DIR=${DATA_DIR}"/labels"

# Repository directory
export P51_REPO_DIR="<PANDEMIC51/PARENT/DIR>"

# MySQL
export P51_SQL_USERNAME="<username>"
export P51_SQL_PASSWORD="<password>"
export P51_SQL_DATABASE_NAME="p51db"

# Login shortcut
alias p51mysql="mysql -u $P51_SQL_USERNAME -p$P51_SQL_PASSWORD $P51_SQL_DATABASE_NAME"
```

Then create a `pandemic51/core/config.py` from the provided template:

```bash
cp config/config-template.py pandemic51/core/config.py
```

You must populate the `{{TODO}}`s in `config.py` with the appropriate values.
Note that many of these need to exactly match the environment variables of the
same name that you set above.

### Virtual environment

We recommend creating a virtual environment for your development work:

```
virtualenv -p /usr/local/bin/python3.6 ${ENV_DIR}/covid19
source ${ENV_DIR}/covid19/bin/activate
```

### Installation

First, follow the instructions in `mac_preinstall.md` for MacOS local
development or run `linux_preinstall.bash` for Linux systems.

Then, run the install script:

```bash
bash install.bash
```

### Initialize the database

```bash
bash database/init_db.bash
```

This can be run at anytime to wipe the database.


### Initialize Celery

Celery is currently only configured for Linux as a `systemd` daemon.

> todo(tyler): make a configuration for MacOS with `launchd`

- Copy the Celery templates in `config/` and replace any `{{ENV_VAR}}` with the
respective environment variable value
- Place `celery.service` & `celerybeat.service` in `/lib/systemd/system`
- Start the services

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

#### Download data

Download the model(s) that you need by running the following script:

```bash
bash download_models.bash
```

Download some historical data to work with by running the following script:

```bash
bash download_historical_data.bash
```


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
