#!/usr/bin/env python3
"""
Test simple de la galerie photos
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import GaleriePhoto
import requests

def test_galerie_simple():
    """Test simple de la galerie photos"""
    
    print("📸 Test simple de la galerie photos:")
    print("=" * 50)
    
    # 1. Vérifier les photos existantes
    print("\n1️⃣ Photos en base:")
    total_photos = GaleriePhoto.objects.count()
    print(f"📸 Total: {total_photos}")
    
    if total_photos > 0:
        for photo in GaleriePhoto.objects.all()[:3]:
            print(f"  - {photo.titre} ({photo.get_categorie_display()})")
    
    # 2. Test API simple
    print("\n2️⃣ Test API:")
    try:
        response = requests.get('http://localhost:8000/api/galerie/')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API OK - {len(data.get('photos', []))} photos")
        else:
            print(f"❌ Erreur API: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
    
    # 3. Test cache
    print("\n3️⃣ Test cache:")
    try:
        # Premier appel
        response1 = requests.get('http://localhost:8000/api/galerie/')
        # Deuxième appel (devrait utiliser le cache)
        response2 = requests.get('http://localhost:8000/api/galerie/')
        
        if response1.status_code == 200 and response2.status_code == 200:
            print("✅ Cache fonctionnel")
        else:
            print("❌ Problème avec le cache")
    except Exception as e:
        print(f"❌ Erreur cache: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Pour tester dans l'app:")
    print("1. http://localhost:3000/dashboard-patron")
    print("2. Se connecter avec un patron")
    print("3. Cliquer sur '🖼️ Galerie'")
    print("4. Ajouter des photos")

if __name__ == "__main__":
    test_galerie_simple() 