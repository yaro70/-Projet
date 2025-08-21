#!/usr/bin/env python3
"""
Test de la galerie photos
"""

import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User, GaleriePhoto
import requests
import json

def test_galerie():
    """Test de la galerie photos"""
    
    print("📸 Test de la galerie photos:")
    print("=" * 60)
    
    # 1. Vérifier les photos existantes
    print("\n1️⃣ Vérification des photos existantes:")
    total_photos = GaleriePhoto.objects.count()
    print(f"📸 Total photos: {total_photos}")
    
    if total_photos > 0:
        print("\n📋 Photos disponibles:")
        for photo in GaleriePhoto.objects.all():
            print(f"  📸 {photo.titre} (ID: {photo.id})")
            print(f"    📂 Catégorie: {photo.get_categorie_display()}")
            print(f"    📅 Date: {photo.date_realisation}")
            print(f"    🖼️ Image: {'Oui' if photo.image else 'Non'}")
    else:
        print("ℹ️ Aucune photo disponible")
    
    # 2. Test de l'API publique
    print("\n2️⃣ Test de l'API publique de la galerie:")
    
    try:
        response = requests.get('http://localhost:8000/api/galerie/')
        
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Galerie récupérée avec succès!")
            print(f"📸 Nombre de photos: {len(data['photos'])}")
            print(f"📂 Catégories disponibles: {data['categories']}")
            
            if data['photos']:
                print("\n📋 Détails des photos (API):")
                for photo in data['photos'][:3]:  # Afficher seulement les 3 premières
                    print(f"  📸 {photo['titre']} (ID: {photo['id']})")
                    print(f"    📂 Catégorie: {photo['categorie_display']}")
                    print(f"    📅 Date: {photo['date_realisation']}")
                    if photo['image']:
                        print(f"    🖼️ Image: {photo['image']}")
                    else:
                        print(f"    🖼️ Image: Aucune")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération: {e}")
    
    # 3. Test de filtrage par catégorie
    print("\n3️⃣ Test de filtrage par catégorie:")
    
    try:
        response = requests.get('http://localhost:8000/api/galerie/?categorie=anniversaire')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filtrage par catégorie 'anniversaire': {len(data['photos'])} photos")
        else:
            print(f"❌ Erreur lors du filtrage: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de filtrage: {e}")
    
    # 4. Test d'ajout de photo (patron seulement)
    print("\n4️⃣ Test d'ajout de photo (patron seulement):")
    
    try:
        # Connexion patron
        login_data = {
            'username': 'deliceDek@ty',
            'password': 'delicedek@ty123'
        }
        
        login_response = requests.post('http://localhost:8000/api/login/', data=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            print(f"✅ Connexion patron réussie")
            
            # Test d'ajout de photo
            headers = {'Authorization': f'Token {token}'}
            
            # Note: On ne peut pas tester l'upload d'image sans fichier réel
            # Mais on peut tester la structure de l'API
            print("ℹ️ Test de structure de l'API d'ajout (sans fichier)")
            print("📋 Endpoint: POST /api/galerie/ajouter/")
            print("📋 Champs requis: titre, date_realisation, image")
            print("📋 Champs optionnels: description, categorie, ordre_affichage")
            
        else:
            print(f"❌ Échec de connexion patron: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'ajout: {e}")
    
    # 5. Test de création d'une photo en base
    print("\n5️⃣ Test de création d'une photo en base:")
    
    try:
        photo = GaleriePhoto.objects.create(
            titre="Gâteau de Mariage Élégant",
            description="Un magnifique gâteau de mariage à 3 étages avec des décorations florales",
            categorie="mariage",
            date_realisation="2025-07-28",
            ordre_affichage=2
        )
        
        print(f"✅ Photo créée: #{photo.id}")
        print(f"📰 Titre: {photo.titre}")
        print(f"📂 Catégorie: {photo.get_categorie_display()}")
        print(f"📅 Date: {photo.date_realisation}")
        
        # Vérifier l'API après création
        response = requests.get('http://localhost:8000/api/galerie/')
        if response.status_code == 200:
            data = response.json()
            print(f"📸 Total photos après création: {len(data['photos'])}")
        
        # Nettoyer
        photo.delete()
        print("🧹 Photo de test supprimée")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("1. Aller sur http://localhost:3000/dashboard-patron")
    print("2. Se connecter avec un compte patron")
    print("3. Cliquer sur '🖼️ Galerie' dans la sidebar")
    print("4. Ajouter des photos avec le bouton +")
    print("5. Voir la galerie publique sur la page d'accueil")

if __name__ == "__main__":
    test_galerie() 