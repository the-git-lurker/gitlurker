#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations git_lurker --no-input
python manage.py migrate git_lurker
python manage.py loaddata initial_projects_categorised.json
# python manage.py createsuperuser --noinput
