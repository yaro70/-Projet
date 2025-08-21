#!/usr/bin/env python3
import os
import django
import requests

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau

def test_images():
    """Test des images des gâteaux"""
    
    print("🖼️  Test des images des gâteaux:")
    print("=" * 40)
    
    # 1. Vérifier les gâteaux en base
    print("\n1️⃣ Gâteaux en base de données:")
    gateaux = Gateau.objects.all()
    print(f"   📊 Nombre de gâteaux: {gateaux.count()}")
    
    for gateau in gateaux:
        print(f"   🎂 {gateau.nom}:")
        print(f"      - Image: {gateau.image}")
        print(f"      - URL complète: http://localhost:8000{gateau.image}" if gateau.image else "      - Aucune image")
        print(f"      - Prix: {gateau.prix} FCFA")
        print()
    
    # 2. Test API publique
    print("\n2️⃣ Test API publique gâteaux:")
    try:
        response = requests.get('http://localhost:8000/api/public/gateaux/')
        if response.status_code == 200:
            gateaux_api = response.json()
            print(f"   ✅ {len(gateaux_api)} gâteau(x) récupéré(s)")
            
            for gateau in gateaux_api:
                print(f"   🎂 {gateau['nom']}:")
                print(f"      - Image: {gateau.get('image', 'Aucune')}")
                print(f"      - URL complète: http://localhost:8000{gateau.get('image', '')}" if gateau.get('image') else "      - Aucune image")
                print()
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Test accès direct aux images
    print("\n3️⃣ Test accès direct aux images:")
    for gateau in gateaux:
        if gateau.image:
            try:
                image_url = f"http://localhost:8000{gateau.image}"
                response = requests.head(image_url)
                if response.status_code == 200:
                    print(f"   ✅ {gateau.nom}: Image accessible")
                else:
                    print(f"   ❌ {gateau.nom}: Image non accessible ({response.status_code})")
            except Exception as e:
                print(f"   ❌ {gateau.nom}: Erreur d'accès - {e}")
        else:
            print(f"   ⚠️  {gateau.nom}: Aucune image")
    
    print("\n🎉 Test des images terminé!")

if __name__ == '__main__':
    test_images() 