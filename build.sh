#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate git_lurker zero
python manage.py migrate
python manage.py dumpdata git_lurker.project > initial_projects.json
python manage.py createsuperuser --noinput