# pandemic51

Voxel51's website for monitoring the impact of the coronavirus pandemic.


## Installation

### Basic setup

```bash
bash install.bash
```

Download the model(s) that you need via the `download_models.py` script.


### Local MySQL configuration

#### 1) Install `mysql` (MacOS)

Install `mysql` using [homebrew](https://brew.sh/).

You can start/stop the service via:

```
brew services start mysql
brew services stop mysql
```

#### 2) Create the database

Put the following at the bottom of your `~/.bash_profile` or `~/.bashrc` where
`<USERNAME>`, `<PASSWORD>`, etc. are placeholders.

```
export P51_SQL_USERNAME="<USERNAME>"
export P51_SQL_PASSWORD="<PASSWORD>"
export P51_SQL_DATABASE_NAME="<DATABASE>"

# login shortcut command
alias p51mysql="mysql -u $P51_SQL_USERNAME -p$P51_SQL_PASSWORD $P51_SQL_DATABASE_NAME"
```

Now create the database using the same username, password, etc.

```bash
mysql -u root -p
```

```
create database <DATABASE>;
create user '<USERNAME>'@'localhost' identified by '<PASSWORD>';
grant all privileges on <DATABASE>.* to '<USERNAME>'@'localhost';
exit
```

#### 3) Initialize the Database:
```bash
p51mysql < database/init.sql
```

If you want to refresh the database, the commands to drop tables are commented
out in `database/init.sql`.


## Quickstart

Check out the following resources:

- `tests/start/`: simple tests of the initial functionality
- `tests/download_and_store/`: combines `test/start/` with DB communication
- `tests/density`: example of backend person detection on images


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
