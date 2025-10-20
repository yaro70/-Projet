#!/bin/bash
"""
Script de déploiement pour Render
"""

set -e

echo "🚀 Déploiement du Projet Pâtisserie sur Render"
echo "=============================================="

# Vérifier que nous sommes dans le bon répertoire
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Veuillez exécuter ce script depuis la racine du projet"
    exit 1
fi

# Configuration backend
echo "🔧 Configuration du backend..."
cd backend

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer les données de test
echo "📝 Création des données de test..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')
django.setup()

from django.contrib.auth import get_user_model
from boutique.models import *
from decimal import Decimal

User = get_user_model()

# Créer superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser créé: admin/admin123')

# Créer gâteaux
if Gateau.objects.count() == 0:
    gateaux_data = [
        {'nom': 'Gâteau d\'Anniversaire Chocolat', 'description': 'Délicieux gâteau au chocolat', 'prix': Decimal('15000.00')},
        {'nom': 'Gâteau de Mariage Vanille', 'description': 'Magnifique gâteau de mariage', 'prix': Decimal('25000.00')},
        {'nom': 'Cupcakes Assortis', 'description': 'Assortiment de cupcakes', 'prix': Decimal('8000.00')},
    ]
    
    for data in gateaux_data:
        Gateau.objects.create(**data)
    print(f'✅ {len(gateaux_data)} gâteaux créés')

# Créer paramètres
if ParametresLivraison.objects.count() == 0:
    ParametresLivraison.objects.create(prix_livraison=Decimal('2000.00'))
    print('✅ Paramètres de livraison créés')

# Créer utilisateurs
if User.objects.filter(is_patron=True).count() == 0:
    User.objects.create_user('patron', 'patron@example.com', 'patron123', is_patron=True)
    print('✅ Patron créé: patron/patron123')

if User.objects.filter(is_collaborateur=True).count() == 0:
    User.objects.create_user('collaborateur', 'collaborateur@example.com', 'collaborateur123', is_collaborateur=True)
    print('✅ Collaborateur créé: collaborateur/collaborateur123')
"

echo "🎉 Déploiement terminé avec succès!"

