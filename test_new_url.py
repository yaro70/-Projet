#!/usr/bin/env python3
import requests
import json

def test_new_url():
    """Test avec la nouvelle URL"""
    
    print("🆕 Test avec la nouvelle URL:")
    print("=" * 30)
    
    # Test création de commande avec nouvelle URL
    data = {
        'gateau_id': 12,
        'client_nom': 'Test Client',
        'client_telephone': '0123456789',
        'texte_sur_gateau': 'Test commande',
        'date_livraison': '2025-07-29T15:00',
        'livraison': True
    }
    
    print(f"📤 Données envoyées:")
    print(json.dumps(data, indent=2))
    
    try:
        response = requests.post('http://localhost:8000/api/create-commande/', 
                               json=data, 
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        print(f"\n📥 Réponse:")
        print(f"   Statut: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Succès!")
            print(f"   📋 Données: {json.dumps(result, indent=2)}")
        else:
            print(f"   ❌ Erreur!")
            print(f"   📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    test_new_url() 