#!/bin/bash
set -e

#Initializing database data for the first time.
function init_data() {
  FIRST_TIME_STARTUP_PLACEHOLDER="FIRST_TIME_STARTUP_PLACEHOLDER"
  if [ ! -e $FIRST_TIME_STARTUP_PLACEHOLDER ]; then
    echo "---->Initializing database data for the first time startup."
    sql=$(pwd)"/scripts/init_data.sql"
    mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD <$sql
    echo "<----Finished initializing database data."
    touch $FIRST_TIME_STARTUP_PLACEHOLDER
  fi
}

init_data

nohup python /data/src/manage.py runserver --host 0.0.0.0
tail -f /dev/null
exec "$@"
