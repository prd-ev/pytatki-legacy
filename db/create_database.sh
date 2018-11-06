#!/bin/bash

if [ $# -ne 3 ]; then
  echo "Usage: create_database.sh db_user db_password db_name";
  exit 1;
fi

echo "Database name: $3"
rm -r temp
mkdir temp
rm render.txt
echo "db/create_database.sql" >> render.txt
echo "SOURCE db/create_tables.sql" >> render.txt

for fp in db/views/*; do
  echo "$fp" >> render.txt
done

#. db/render_scripts.py "$3"