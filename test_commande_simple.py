#!/usr/bin/env python3
import requests
import json

def test_commande_simple():
    """Test simple de création de commande"""
    
    print("🧪 Test simple de création de commande:")
    print("=" * 40)
    
    # Données de test
    data = {
        'gateau_id': 12,  # ID du gâteau que vous avez sélectionné
        'client_nom': 'Test Client',
        'client_telephone': '0123456789',
        'texte_sur_gateau': 'Test commande',
        'date_livraison': '2025-07-29T15:00',
        'livraison': True
    }
    
    print(f"📤 Données envoyées:")
    print(json.dumps(data, indent=2))
    
    try:
        response = requests.post('http://localhost:8000/api/commandes/create/', 
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
    test_commande_simple() 