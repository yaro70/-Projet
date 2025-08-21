#!/usr/bin/env python
"""
Script pour corriger la base de données et les migrations
"""

import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from boutique.models import *

def fix_database():
    print("🔧 Correction de la base de données...")
    print("=" * 50)
    
    try:
        # Vérifier la connexion
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        print("✅ Connexion base de données OK")
        
        # Créer les migrations
        print("📝 Création des migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'boutique'])
        
        # Appliquer les migrations
        print("📝 Application des migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Vérifier les tables
        print("🔍 Vérification des tables...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE 'boutique_%'
            """)
            tables = cursor.fetchall()
            print(f"📋 Tables trouvées: {[table[0] for table in tables]}")
        
        # Vérifier la structure de la table Gateau
        print("🔍 Vérification de la table Gateau...")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(boutique_gateau)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            print(f"📋 Colonnes: {column_names}")
            
            if 'date_creation' not in column_names:
                print("⚠️ Colonne date_creation manquante, ajout...")
                cursor.execute("ALTER TABLE boutique_gateau ADD COLUMN date_creation DATETIME")
                print("✅ Colonne date_creation ajoutée")
        
        # Mettre à jour les gâteaux existants
        print("🔄 Mise à jour des gâteaux existants...")
        from django.utils import timezone
        Gateau.objects.all().update(date_creation=timezone.now())
        print("✅ Gâteaux mis à jour")
        
        # Vérifier les données
        print("📊 Vérification des données...")
        gateaux_count = Gateau.objects.count()
        print(f"🎂 Gâteaux: {gateaux_count}")
        
        parametres_count = ParametresLivraison.objects.count()
        print(f"⚙️ Paramètres: {parametres_count}")
        
        users_count = User.objects.count()
        print(f"👥 Utilisateurs: {users_count}")
        
        print("🎉 Correction terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_database()
