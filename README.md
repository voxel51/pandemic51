# pandemic51
Voxel51's website for monitoring the impact of the coronavirus pandemic

## Installation:

Before running the installation script, following the instructions in
`mac_preinstall.md` for Mac local development or run `linux_preinstall.bash`
for linux systems.

```bash
bash install.bash
```

## Local MySQL Configuration:

### 1) Create the database

Put the following at the bottom of your `~/.bash_profile` or `~/.bashrc` where
`<USERNAME>`, `<PASSWORD>`, etc. are placeholders.

```
export P51_SQL_USERNAME="<USERNAME>"
export P51_SQL_PASSWORD="<PASSWORD>"
export P51_SQL_DATABASE_NAME="pandemic51"

# login shortcut command
alias p51mysql="mysql -u $P51_SQL_USERNAME -p$P51_SQL_PASSWORD $P51_SQL_DATABASE_NAME"
```

Now create the database using the same username, password, etc.

```bash
mysql -u root -p
```

```
create database pandemic51;
create user '<USERNAME>'@'localhost' identified by '<PASSWORD>';
grant all privileges on pandemic51.* to '<USERNAME>'@'localhost';
exit
```

### 2) Initialize the Database:
```bash
p51mysql < database/init.sql
```

If you want to refresh the database, the commands to drop tables are commented
out in `database/init.sql`.


## Starting Point

Check `tests/start/` for some simple tests of the initial functionality.

`tests/download_and_store/` combines this functionality and communicates with
the database.


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
