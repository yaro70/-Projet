#!/usr/bin/env python3
import os
import django
import requests

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau, ParametresLivraison

def test_permissions():
    """Test des permissions de l'API"""
    
    print("🔐 Test des permissions de l'API:")
    print("=" * 50)
    
    # Test 1: API publique gâteaux (devrait fonctionner)
    print("\n1️⃣ Test API publique gâteaux:")
    try:
        response = requests.get('http://localhost:8000/api/public/gateaux/')
        if response.status_code == 200:
            gateaux = response.json()
            print(f"   ✅ API publique gâteaux: {len(gateaux)} gâteaux")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: API gâteaux (devrait fonctionner)
    print("\n2️⃣ Test API gâteaux:")
    try:
        response = requests.get('http://localhost:8000/api/gateaux/')
        if response.status_code == 200:
            gateaux = response.json()
            print(f"   ✅ API gâteaux: {len(gateaux)} gâteaux")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: API paramètres (devrait fonctionner)
    print("\n3️⃣ Test API paramètres:")
    try:
        response = requests.get('http://localhost:8000/api/parametres/')
        if response.status_code == 200:
            params = response.json()
            print(f"   ✅ API paramètres: {len(params)} paramètre(s)")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4: API commandes (devrait échouer sans authentification)
    print("\n4️⃣ Test API commandes (sans authentification):")
    try:
        response = requests.get('http://localhost:8000/api/commandes/')
        if response.status_code == 401:
            print("   ✅ API commandes: Accès refusé (normal sans authentification)")
        else:
            print(f"   ⚠️  Statut inattendu: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test des permissions terminé!")

if __name__ == '__main__':
    test_permissions() 