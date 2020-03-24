#!/usr/bin/env bash

echo "Configuring MYSQL"

sudo mysql -u root -e "DROP DATABASE IF EXISTS $P51_SQL_DATABASE_NAME;"
sudo mysql -u root -e "CREATE DATABASE $P51_SQL_DATABASE_NAME;"

sudo mysql -u root -e "DROP USER IF EXISTS '$P51_SQL_USERNAME'@'localhost';"
sudo mysql -u root -e "CREATE USER '$P51_SQL_USERNAME'@'localhost' IDENTIFIED BY '$P51_SQL_PASSWORD';"
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON $P51_SQL_DATABASE_NAME.* TO '$P51_SQL_USERNAME'@'localhost';"
sudo mysql -u root -e "FLUSH PRIVILEGES;"

mysql -u $P51_SQL_USERNAME -p$P51_SQL_PASSWORD $P51_SQL_DATABASE_NAME < database/init_tables.sql
