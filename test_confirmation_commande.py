#!/usr/bin/env python3
import requests
import json

def test_confirmation_commande():
    """Test de l'étape de confirmation de commande"""
    
    print("🎉 Test de l'étape de confirmation de commande:")
    print("=" * 50)
    
    # 1. Récupérer un gâteau pour le test
    print("\n1️⃣ Récupération d'un gâteau:")
    try:
        response = requests.get('http://localhost:8000/api/public/gateaux/')
        if response.status_code == 200:
            gateaux = response.json()
            if gateaux:
                gateau = gateaux[0]
                print(f"   ✅ Gâteau sélectionné: {gateau['nom']} - {gateau['prix']} FCFA")
            else:
                print("   ❌ Aucun gâteau disponible")
                return
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return
    
    # 2. Récupérer les paramètres de livraison
    print("\n2️⃣ Récupération des paramètres de livraison:")
    try:
        response = requests.get('http://localhost:8000/api/parametres/')
        if response.status_code == 200:
            parametres = response.json()
            if parametres:
                prix_livraison = parametres[0]['prix_livraison']
                print(f"   ✅ Prix de livraison: {prix_livraison} FCFA")
            else:
                print("   ⚠️  Aucun paramètre de livraison")
                prix_livraison = 0
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
            prix_livraison = 0
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        prix_livraison = 0
    
    # 3. Simuler une commande
    print("\n3️⃣ Simulation d'une commande:")
    commande_data = {
        'gateau_id': gateau['id'],
        'client_nom': 'Test Client',
        'client_telephone': '0123456789',
        'texte_sur_gateau': 'Joyeux Anniversaire!',
        'date_livraison': '2025-07-29T15:00:00',
        'livraison': True
    }
    
    print(f"   📋 Données de commande:")
    print(f"      - Gâteau: {gateau['nom']}")
    print(f"      - Client: {commande_data['client_nom']}")
    print(f"      - Téléphone: {commande_data['client_telephone']}")
    print(f"      - Livraison: {'Oui' if commande_data['livraison'] else 'Non'}")
    print(f"      - Prix total: {float(gateau['prix']) + (prix_livraison if commande_data['livraison'] else 0)} FCFA")
    
    # 4. Test de création de commande
    print("\n4️⃣ Test de création de commande:")
    try:
        response = requests.post('http://localhost:8000/api/create-commande/', json=commande_data)
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Commande créée avec succès!")
            print(f"   📋 ID: {result.get('commande_id')}")
            print(f"   💰 Prix total: {result.get('prix_total')} FCFA")
        else:
            print(f"   ❌ Erreur: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("   1. Aller sur http://localhost:3000")
    print("   2. Sélectionner un gâteau et cliquer 'Commander'")
    print("   3. Remplir le formulaire")
    print("   4. Cliquer 'Confirmer la commande'")
    print("   5. Vérifier l'étape de confirmation avec le message de paiement")
    print("   6. Tester le bouton WhatsApp")

if __name__ == '__main__':
    test_confirmation_commande() 