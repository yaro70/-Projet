#!/usr/bin/env python
"""
Script pour configurer les données après déploiement
"""

import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')
django.setup()

from django.contrib.auth import get_user_model
from boutique.models import *

def setup_data():
    print("🔧 Configuration des données...")
    
    # Créer superuser
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Superuser créé: admin/admin123")
    
    # Créer gâteaux
    if Gateau.objects.count() == 0:
        gateaux_data = [
            {'nom': 'Gâteau d\'Anniversaire Chocolat', 'description': 'Délicieux gâteau au chocolat', 'prix': Decimal('15000.00')},
            {'nom': 'Gâteau de Mariage Vanille', 'description': 'Magnifique gâteau de mariage', 'prix': Decimal('25000.00')},
            {'nom': 'Cupcakes Assortis', 'description': 'Assortiment de cupcakes', 'prix': Decimal('8000.00')},
        ]
        
        for data in gateaux_data:
            Gateau.objects.create(**data)
        print(f"✅ {len(gateaux_data)} gâteaux créés")
    
    # Créer paramètres
    if ParametresLivraison.objects.count() == 0:
        ParametresLivraison.objects.create(prix_livraison=Decimal('2000.00'))
        print("✅ Paramètres de livraison créés")
    
    # Créer utilisateurs
    if User.objects.filter(is_patron=True).count() == 0:
        User.objects.create_user('patron', 'patron@example.com', 'patron123', is_patron=True)
        print("✅ Patron créé: patron/patron123")
    
    if User.objects.filter(is_collaborateur=True).count() == 0:
        User.objects.create_user('collaborateur', 'collaborateur@example.com', 'collaborateur123', is_collaborateur=True)
        print("✅ Collaborateur créé: collaborateur/collaborateur123")
    
    print("🎉 Configuration terminée!")

if __name__ == '__main__':
    setup_data()
