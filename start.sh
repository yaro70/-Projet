#!/bin/bash
echo "Starting Django application..."
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "PORT: $PORT"
echo "Current directory: $(pwd)"
echo "Files in current directory: $(ls -la)"

# Démarrer Gunicorn avec la bonne configuration
exec gunicorn patisserie_project.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
