#!/bin/bash
echo "Starting migration"
flask db init
flask db migrate
flask db upgrade
echo "Starting telegram bot after migration complition"
export START_BOT=start
exec gunicorn -w 4 -b :5000 --access-logfile - --error-logfile - app:app
