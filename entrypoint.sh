#!/bin/sh 
set -e
echo "🔄 Running migrations ..."
python manage.py migrate --noinput

echo "Creating superuser if needed"
python create_superuser.py

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting gunicorn $PORT"
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2