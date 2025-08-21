#!/usr/bin/env python
"""
Script pour recréer la base de données proprement
"""

import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line
from boutique.models import *

def reset_database():
    print("🔄 Réinitialisation de la base de données...")
    
    # Supprimer et recréer les migrations
    print("📝 Suppression des anciennes migrations...")
    try:
        import shutil
        migrations_dir = 'boutique/migrations'
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                if file.endswith('.py') and file != '__init__.py':
                    os.remove(os.path.join(migrations_dir, file))
        print("✅ Anciennes migrations supprimées")
    except Exception as e:
        print(f"⚠️ Erreur lors de la suppression des migrations: {e}")
    
    # Créer de nouvelles migrations
    print("📝 Création de nouvelles migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'boutique', '--noinput'])
        print("✅ Nouvelles migrations créées")
    except Exception as e:
        print(f"⚠️ Erreur lors de la création des migrations: {e}")
    
    # Appliquer les migrations
    print("📝 Application des migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations appliquées")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'application des migrations: {e}")
    
    # Créer les données de test
    print("📝 Création des données de test...")
    
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
    
    print("🎉 Base de données réinitialisée avec succès!")

if __name__ == '__main__':
    reset_database()
