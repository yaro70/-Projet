#!/usr/bin/env python
"""
Script final pour corriger la base de données
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')
django.setup()

from django.db import connection

def fix_database():
    print("🔧 Correction finale de la base de données...")
    
    try:
        with connection.cursor() as cursor:
            # Vérifier la structure de la table Gateau
            cursor.execute("PRAGMA table_info(boutique_gateau)")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"Colonnes actuelles de Gateau: {columns}")
            
            # Ajouter date_creation si elle n'existe pas
            if 'date_creation' not in columns:
                print("📝 Ajout de date_creation à Gateau...")
                cursor.execute("ALTER TABLE boutique_gateau ADD COLUMN date_creation DATETIME DEFAULT CURRENT_TIMESTAMP")
                print("✅ date_creation ajoutée")
            
            # Vérifier la structure de la table ArticleEvenement
            cursor.execute("PRAGMA table_info(boutique_articleevenement)")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"Colonnes actuelles de ArticleEvenement: {columns}")
            
            # Ajouter les colonnes manquantes
            if 'contenu' not in columns:
                print("📝 Ajout de contenu à ArticleEvenement...")
                cursor.execute("ALTER TABLE boutique_articleevenement ADD COLUMN contenu TEXT")
                print("✅ contenu ajouté")
            
            if 'date_evenement' not in columns:
                print("📝 Ajout de date_evenement à ArticleEvenement...")
                cursor.execute("ALTER TABLE boutique_articleevenement ADD COLUMN date_evenement DATETIME")
                print("✅ date_evenement ajouté")
            
            if 'actif' not in columns:
                print("📝 Ajout de actif à ArticleEvenement...")
                cursor.execute("ALTER TABLE boutique_articleevenement ADD COLUMN actif BOOLEAN DEFAULT 1")
                print("✅ actif ajouté")
            
            # Vérifier les données existantes
            cursor.execute("SELECT COUNT(*) FROM boutique_gateau")
            gateau_count = cursor.fetchone()[0]
            print(f"📊 Nombre de gâteaux: {gateau_count}")
            
            cursor.execute("SELECT COUNT(*) FROM boutique_parametreslivraison")
            param_count = cursor.fetchone()[0]
            print(f"📊 Nombre de paramètres: {param_count}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    print("🎉 Correction de la base de données terminée!")
    return True

if __name__ == '__main__':
    fix_database()
