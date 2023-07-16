#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate
python manage.py loaddata initial_projects.json
python manage.py createsuperuser --noinput