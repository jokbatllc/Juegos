#!/usr/bin/env bash
set -e
python manage.py collectstatic --noinput || true
python manage.py migrate --noinput
exec "$@"
