#!/usr/bin/env bash
# Script de démarrage pour Render

echo "🚀 Démarrage de l'application..."

# Vérifier les variables d'environnement
echo "📋 Variables d'environnement:"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DEBUG: $DEBUG"
echo "PORT: $PORT"

# Démarrer Gunicorn
echo "🐍 Démarrage de Gunicorn..."
exec gunicorn patisserie_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --workers 2 \
    --access-logfile - \
    --error-logfile -
