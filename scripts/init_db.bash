#!/usr/bin/env bash
# Initializes the database.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#

echo "***** CONFIGURING MYSQL *****"

sudo mysql -u root -e "DROP DATABASE IF EXISTS $P51_SQL_DATABASE_NAME;"
sudo mysql -u root -e "CREATE DATABASE $P51_SQL_DATABASE_NAME;"

sudo mysql -u root -e "DROP USER IF EXISTS '$P51_SQL_USERNAME'@'localhost';"
sudo mysql -u root -e "CREATE USER '$P51_SQL_USERNAME'@'localhost' IDENTIFIED BY '$P51_SQL_PASSWORD';"
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON $P51_SQL_DATABASE_NAME.* TO '$P51_SQL_USERNAME'@'localhost';"
sudo mysql -u root -e "FLUSH PRIVILEGES;"

mysql -u $P51_SQL_USERNAME -p$P51_SQL_PASSWORD $P51_SQL_DATABASE_NAME < scripts/init_tables.sql
