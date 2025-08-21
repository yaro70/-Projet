#!/usr/bin/env python3
import requests
import time

def test_quick():
    """Test rapide des APIs"""
    
    print("⚡ Test rapide des APIs:")
    print("=" * 30)
    
    # Attendre un peu que le serveur se recharge
    print("⏳ Attente du rechargement du serveur...")
    time.sleep(3)
    
    # Test 1: API publique gâteaux
    print("\n1️⃣ Test API publique gâteaux:")
    try:
        response = requests.get('http://localhost:8000/api/public/gateaux/', timeout=5)
        if response.status_code == 200:
            gateaux = response.json()
            print(f"   ✅ {len(gateaux)} gâteaux disponibles")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: API paramètres
    print("\n2️⃣ Test API paramètres:")
    try:
        response = requests.get('http://localhost:8000/api/parametres/', timeout=5)
        if response.status_code == 200:
            params = response.json()
            print(f"   ✅ {len(params)} paramètre(s) disponible(s)")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test rapide terminé!")

if __name__ == '__main__':
    test_quick() 