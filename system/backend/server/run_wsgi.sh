#!/bin/sh
echo "Starting the WSGI Server"
exec gunicorn --bind 0.0.0.0:8000 run:app
