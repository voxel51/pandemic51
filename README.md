# pandemic51

Voxel51's website for monitoring the impact of the Coronavirus pandemic.
See it live at https://pdi.voxel51.com.

<img src="https://user-images.githubusercontent.com/3719547/74191434-8fe4f500-4c21-11ea-8d73-555edfce0854.png" alt="voxel51-logo.png" width="40%"/>


## Organization

```
.
├── api                      <-- API definition
├── config                   <-- config files and templates
├── pandemic51               <-- core backend libary
├── README.md                <-- this README
├── scripts                  <-- handy scripts
└── web                      <-- web client
```


## Installation

### Clone the repository

```bash
git clone https://github.com/voxel51/pandemic51
```

### Environment variables and configuration

Add the following to your `~/.bash_profile` or `~/.bashrc`, setting `{{CWD}}`
to your current working directory and setting your MySQL username and password:

```bash
# Pandemic51 resources
export P51_BASE_DIR="{{CWD}}"
export P51_REPO_DIR="${P51_BASE_DIR}/pandemic51"
export P51_CELERY_DIR="${P51_BASE_DIR}/celery"
export P51_DATA_DIR="${P51_BASE_DIR}/data"
export P51_SQL_USERNAME="{{USERNAME}}"
export P51_SQL_PASSWORD="{{PASSWORD}}"
export P51_SQL_DATABASE_NAME=p51db

# Login shortcut
alias p51mysql="mysql -u ${P51_SQL_USERNAME} -p ${P51_SQL_PASSWORD} ${P51_SQL_DATABASE_NAME}"
```

With the above in-place, `source` your config to apply the changes.

Next, create a `pandemic51/config.py` from the provided template:

```bash
cp config/config-template.py pandemic51/config.py
```

and customize any values as needed. Be sure to match `P51_SQL_USERNAME` and 
`P51_SQL_PASSWORD` to the values you set to your environment variables.

### Pre-installation

For Linux users, run the `scripts/linux_preinstall.bash` script.

> todo: finish MacOS preinstall script

We strongly recommend creating a virtual environment for your development work:

```bash
ENV_DIR=/path/for/your/venv

virtualenv -p /usr/local/bin/python3.6 ${ENV_DIR}/covid19
source ${ENV_DIR}/covid19/bin/activate
```

### Installation

Run the install script:

```bash
bash install.bash
```

### Initialize the database

```bash
bash scripts/init_db.bash
```

This can be run at anytime to wipe the database.

### Initialize Celery

Celery is configured for Linux as a `systemd` daemon.

> todo: make a configuration for MacOS with `launchd`

First, create copies of the Celery templates:

```bash
cp config/celery-template.conf config/celery.conf
cp config/celery-template.service config/celery.service
cp config/celerybeat-template.service config/celerybeat.service
```

and fill in all `{{VALUE}}` placeholders with the appropriate values.

Then place `celery.service` & `celerybeat.service` in `/lib/systemd/system`:

```bash
mv config/celery.service /lib/systemd/system
mv config/celerybeat.service /lib/systemd/system
```

and start the services using the instructions below.

#### Cheatsheet

Any time a file is added or modified in `/lib/systemd/system`, run:

```bash
sudo systemctl daemon-reload
```

Control the celery/celerybeat services as follows:

```bash
systemctl {start|stop|restart|status} celery.service celerybeat.service
```

To watch logs:

```bash
tail -f -n 10 ${P51_CELERY_DIR}/worker*
```

### Download data

Download the model(s) that you need by running the following script:

```bash
bash scripts/download_models.bash
```

Download some historical data to work with by running the following script:

```bash
bash scripts/download_historical_data.bash
```


## Copyright

Copyright 2020, Voxel51, Inc.<br>
voxel51.com
