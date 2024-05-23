#!/usr/bin/env sh
set -ex

# Run migrations
/app/manage.py migrate

# Load users
/app/manage.py loadusers

# Start uWSGI processes
exec uwsgi --http :${MUNERA_PORT} /app/uwsgi.ini
