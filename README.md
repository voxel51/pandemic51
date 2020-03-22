# pandemic51
Voxel51's website for monitoring the impact of the coronavirus pandemic


# Local MySQL Configuration:

These instructions are for macOS.


Install `mysql` using [homebrew](https://brew.sh/).

You can start/stop the service via:

```
brew services start mysql
brew services stop mysql
```

Start the service and log in:

```
mysql -u root -p
```

```
create database <DATABASE>;
create user '<USERNAME>'@'localhost' identified by '<PASSWORD>';
grant all privileges on <DATABASE>.* to '<USERNAME>'@'localhost';
exit
```
Put the following at the bottom of your `~/.bash_profile` file:

```
export P51_SQL_USERNAME="<USERNAME>"
export P51_SQL_PASSWORD="<PASSWORD>"
export P51_SQL_DATABASE_NAME="<DATABASE>"

# login shortcut command
alias p51mysql="mysql -u $P51_SQL_USERNAME -p$P51_SQL_PASSWORD $P51_SQL_DATABASE_NAME"
```

and run `source ~/.bash_profile`. You can now call `p51mysql` from the command
line to be logged into mysql as the newly created user.

## Initialize the Database:
```bash
p51mysql < database/init.sql
```
