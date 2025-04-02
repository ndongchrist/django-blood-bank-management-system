#!/bin/bash
pip install -r requirements.txt

python manage.py makemigrations 
python manage.py migrate

echo "Collecting statics..."
echo 'yes' | python manage.py collectstatic --noinput

sleep 5

gunicorn bloodBMS.wsgi:application -b 0.0.0.0:8000 -w 2 --log-level DEBUG --reload --threads=2 --timeout=3600