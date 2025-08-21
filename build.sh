#!/usr/bin/env bash
# Script de build pour Render

set -e  # Arrêter le script en cas d'erreur

echo "🚀 Démarrage du build..."

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Vérifier que Django est installé
echo "🔍 Vérification de Django..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Vérifier la configuration
echo "⚙️ Vérification de la configuration..."
python manage.py check --deploy

# Test de configuration Render
echo "🔧 Test de configuration Render..."
python test_render_config.py

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate

# Créer un superuser si nécessaire (optionnel)
echo "👤 Création d'un superuser par défaut..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser créé: admin/admin123')
else:
    print('Superuser existe déjà')
"

# Vérifier que l'application peut démarrer
echo "🔧 Test de démarrage de l'application..."
python manage.py check

echo "✅ Build terminé avec succès!"

