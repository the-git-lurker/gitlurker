#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py dumpdata git_luker.project --indent 2 > initial_projects.json