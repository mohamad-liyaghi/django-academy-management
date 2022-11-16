#!/bin/bash

echo "Apply database migrations and run"
python manage.py makemigrations && python manage.py migrate && python manage.py runserver --insecure 0.0.0.0:8000