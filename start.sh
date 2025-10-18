#!/usr/bin/env bash
set -e

apt-get update && apt-get install -y postgresql-client

psql "$DATABASE_URL" -f database.sql

exec gunicorn -w 5 -b 0.0.0.0:${PORT:-10000} page_analyzer:app