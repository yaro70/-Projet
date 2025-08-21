#!/usr/bin/env python3
"""
Création et application de la migration pour la galerie photos
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from django.core.management import call_command
import subprocess

def create_galerie_migration():
    """Créer et appliquer la migration pour la galerie photos"""
    
    print("📸 Création et application de la migration de la galerie photos:")
    print("=" * 60)
    
    try:
        # 1. Créer la migration
        print("\n1️⃣ Création de la migration...")
        call_command('makemigrations', 'boutique')
        print("✅ Migration créée avec succès")
        
        # 2. Appliquer la migration
        print("\n2️⃣ Application de la migration...")
        call_command('migrate')
        print("✅ Migration appliquée avec succès")
        
        # 3. Vérifier les modèles
        print("\n3️⃣ Vérification des modèles...")
        from boutique.models import GaleriePhoto
        
        # Vérifier que le modèle existe
        print(f"✅ Modèle GaleriePhoto disponible")
        print(f"📊 Champs: {[field.name for field in GaleriePhoto._meta.fields]}")
        print(f"📂 Catégories: {dict(GaleriePhoto.CATEGORIES)}")
        
        # 4. Test de création d'une photo
        print("\n4️⃣ Test de création d'une photo...")
        
        # Créer une photo de test (sans image pour le moment)
        photo = GaleriePhoto.objects.create(
            titre="Gâteau d'Anniversaire Test",
            description="Un délicieux gâteau d'anniversaire avec des décorations colorées",
            categorie="anniversaire",
            date_realisation="2025-07-29",
            ordre_affichage=1
        )
        
        print(f"✅ Photo créée: #{photo.id}")
        print(f"📰 Titre: {photo.titre}")
        print(f"📂 Catégorie: {photo.get_categorie_display()}")
        print(f"📅 Date: {photo.date_realisation}")
        
        # Nettoyer le test
        photo.delete()
        print("🧹 Photo de test supprimée")
        
        print("\n🎉 Migration de la galerie terminée avec succès!")
        print("\n📋 Prochaines étapes:")
        print("1. Tester l'API: python test_galerie.py")
        print("2. Démarrer le serveur: python manage.py runserver")
        print("3. Tester dans l'application web")
        print("4. Ajouter des photos via le dashboard patron")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_galerie_migration() 