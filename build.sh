#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

reset_db --noinput
python manage.py collectstatic --no-input
python manage.py makemigrations git_lurker --empty
python manage.py makemigrations git_lurker
python manage.py migrate git_lurker
python manage.py loaddata initial_projects.json
# python manage.py createsuperuser --noinput