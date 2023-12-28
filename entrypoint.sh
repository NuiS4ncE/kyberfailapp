#!/bin/bash
python -m pip install --upgrade pip
python -m pip install python3-dotenv

# Make database migrations
echo "Database migrations"
python manage.py makemigrations
python manage.py migrate

# Run app
echo "Starting app"
python manage.py runserver 0.0.0.0:8000