#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: create_database.sh db_name";
  exit 1;
fi

mysql -e 'SET @dbname = "'$1'"; \. db/create_database.sql'
mysql -e 'SET @dbname = "'$1'"; \. db/create_tables.sql'