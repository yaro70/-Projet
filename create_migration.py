#!/usr/bin/env python3
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

def create_migration():
    """Créer et appliquer une migration pour les changements de modèles"""
    
    print("🔧 Création et application de la migration:")
    print("=" * 50)
    
    # Créer la migration
    os.system('python manage.py makemigrations boutique')
    
    # Appliquer la migration
    os.system('python manage.py migrate')
    
    print("✅ Migration créée et appliquée avec succès!")

if __name__ == '__main__':
    create_migration() 