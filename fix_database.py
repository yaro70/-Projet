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
            print(f"📋 Colonnes Gateau: {column_names}")
            
            if 'date_creation' not in column_names:
                print("⚠️ Colonne date_creation manquante, ajout...")
                cursor.execute("ALTER TABLE boutique_gateau ADD COLUMN date_creation DATETIME")
                print("✅ Colonne date_creation ajoutée")
        
        # Vérifier la structure de la table ArticleEvenement
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
        
        # Ajouter les colonnes manquantes pour ArticleEvenement
        missing_columns = []
        if 'date_evenement' not in column_names:
            missing_columns.append("date_evenement DATETIME")
        if 'actif' not in column_names:
            missing_columns.append("actif BOOLEAN DEFAULT 1")
        
        for column_def in missing_columns:
            column_name = column_def.split()[0]
            print(f"⚠️ Colonne {column_name} manquante, ajout...")
            cursor.execute(f"ALTER TABLE boutique_articleevenement ADD COLUMN {column_def}")
            print(f"✅ Colonne {column_name} ajoutée")
        
        # Mettre à jour les gâteaux existants
        print("🔄 Mise à jour des gâteaux existants...")
        from django.utils import timezone
        Gateau.objects.all().update(date_creation=timezone.now())
        print("✅ Gâteaux mis à jour")
        
        # Créer les migrations de manière non-interactive
        print("📝 Création des migrations (non-interactive)...")
        try:
            # Supprimer les anciennes migrations non appliquées
            import os
            migrations_dir = 'boutique/migrations'
            if os.path.exists(migrations_dir):
                for file in os.listdir(migrations_dir):
                    if file.endswith('.py') and file != '__init__.py':
                        file_path = os.path.join(migrations_dir, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            print(f"🗑️ Migration supprimée: {file}")
            
            # Créer une nouvelle migration
            execute_from_command_line(['manage.py', 'makemigrations', 'boutique', '--empty'])
            
            # Créer le contenu de la migration manuellement
            migration_content = '''
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('boutique', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE boutique_gateau ADD COLUMN date_creation DATETIME;",
            "ALTER TABLE boutique_gateau DROP COLUMN date_creation;"
        ),
        migrations.RunSQL(
            "ALTER TABLE boutique_articleevenement ADD COLUMN contenu TEXT;",
            "ALTER TABLE boutique_articleevenement DROP COLUMN contenu;"
        ),
        migrations.RunSQL(
            "ALTER TABLE boutique_articleevenement ADD COLUMN date_evenement DATETIME;",
            "ALTER TABLE boutique_articleevenement DROP COLUMN date_evenement;"
        ),
        migrations.RunSQL(
            "ALTER TABLE boutique_articleevenement ADD COLUMN actif BOOLEAN DEFAULT 1;",
            "ALTER TABLE boutique_articleevenement DROP COLUMN actif;"
        ),
    ]
'''
            
            # Écrire la migration
            migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py']
            if migration_files:
                latest_migration = sorted(migration_files)[-1]
                migration_path = os.path.join(migrations_dir, latest_migration)
                with open(migration_path, 'w') as f:
                    f.write(migration_content)
                print(f"✅ Migration créée: {latest_migration}")
            
        except Exception as e:
            print(f"⚠️ Erreur création migration: {e}")
        
        # Appliquer les migrations
        print("📝 Application des migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
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
