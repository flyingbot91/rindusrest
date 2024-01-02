#!/bin/bash
cd /app
# Fix race condition here
sleep 5;
python manage.py makemigrations;
python manage.py migrate;
python manage.py import_data;
python manage.py runserver 0.0.0.0:8000
