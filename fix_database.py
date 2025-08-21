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
        
        # Vérifier et corriger la table Gateau
        print("🔍 Vérification de la table Gateau...")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(boutique_gateau)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            print(f"📋 Colonnes Gateau: {column_names}")
            
            if 'date_creation' not in column_names:
                print("⚠️ Colonne date_creation manquante, ajout...")
                cursor.execute("ALTER TABLE boutique_gateau ADD COLUMN date_creation DATETIME")
                print("✅ Colonne date_creation ajoutée")
        
        # Vérifier et corriger la table ArticleEvenement
        print("🔍 Vérification de la table ArticleEvenement...")
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(boutique_articleevenement)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            print(f"📋 Colonnes ArticleEvenement: {column_names}")
            
            # Gérer le renommage description -> contenu
            if 'description' in column_names and 'contenu' not in column_names:
                print("⚠️ Renommage description -> contenu...")
                cursor.execute("ALTER TABLE boutique_articleevenement RENAME COLUMN description TO contenu")
                print("✅ Colonne description renommée en contenu")
            elif 'contenu' not in column_names:
                print("⚠️ Colonne contenu manquante, ajout...")
                cursor.execute("ALTER TABLE boutique_articleevenement ADD COLUMN contenu TEXT")
                print("✅ Colonne contenu ajoutée")
            
            # Ajouter les autres colonnes manquantes
            if 'date_evenement' not in column_names:
                print("⚠️ Colonne date_evenement manquante, ajout...")
                cursor.execute("ALTER TABLE boutique_articleevenement ADD COLUMN date_evenement DATETIME")
                print("✅ Colonne date_evenement ajoutée")
            
            if 'actif' not in column_names:
                print("⚠️ Colonne actif manquante, ajout...")
                cursor.execute("ALTER TABLE boutique_articleevenement ADD COLUMN actif BOOLEAN DEFAULT 1")
                print("✅ Colonne actif ajoutée")
        
        # Mettre à jour les gâteaux existants
        print("🔄 Mise à jour des gâteaux existants...")
        from django.utils import timezone
        Gateau.objects.all().update(date_creation=timezone.now())
        print("✅ Gâteaux mis à jour")
        
        # Appliquer les migrations Django
        print("📝 Application des migrations Django...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
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
