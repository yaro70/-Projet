#!/usr/bin/env python3
import requests
import json

def test_permissions_detailed():
    """Test détaillé des permissions"""
    
    print("🔐 Test détaillé des permissions:")
    print("=" * 40)
    
    # Test 1: Vue de test des permissions
    print("\n1️⃣ Test vue permissions:")
    try:
        response = requests.get('http://localhost:8000/api/test-permissions/')
        print(f"   Statut: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Succès: {json.dumps(result, indent=2)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: API publique gâteaux
    print("\n2️⃣ Test API publique gâteaux:")
    try:
        response = requests.get('http://localhost:8000/api/public/gateaux/')
        print(f"   Statut: {response.status_code}")
        if response.status_code == 200:
            gateaux = response.json()
            print(f"   ✅ Succès: {len(gateaux)} gâteaux")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Création de commande (devrait échouer avec 401)
    print("\n3️⃣ Test création de commande:")
    try:
        data = {
            'gateau_id': 12,
            'client_nom': 'Test Client',
            'client_telephone': '0123456789',
            'texte_sur_gateau': 'Test commande',
            'date_livraison': '2025-07-29T15:00',
            'livraison': True
        }
        
        response = requests.post('http://localhost:8000/api/commandes/create/', 
                               json=data, 
                               headers={'Content-Type': 'application/json'})
        
        print(f"   Statut: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Succès: {json.dumps(result, indent=2)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test terminé!")

if __name__ == '__main__':
    test_permissions_detailed() 