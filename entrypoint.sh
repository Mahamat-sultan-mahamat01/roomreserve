#!/bin/sh 
set -e
echo "🔄 Running migrations ..."
python manager.py migrate --noinput

echo "Collecting static files..."
python manager.py collectstatic --noinput

echo "🚀 Starting gunicorn $SPORT"
exec gunicorn config.wsgi.application --bind 0.0.0.0:$SPORT --workers 2