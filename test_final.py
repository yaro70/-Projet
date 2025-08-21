#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau, ParametresLivraison

def test_final():
    """Test final de l'application"""
    
    print("🎯 Test final de l'application:")
    print("=" * 50)
    
    # Vérifier les données
    gateau = Gateau.objects.first()
    parametres = ParametresLivraison.objects.first()
    
    if not gateau:
        print("❌ Aucun gâteau trouvé")
        return
    
    if not parametres:
        print("❌ Aucun paramètre de livraison trouvé")
        return
    
    print(f"🎂 Gâteau: {gateau.nom} - {gateau.prix} FCFA")
    print(f"🚚 Livraison: {parametres.prix_livraison} FCFA")
    
    # Test 1: API publique gâteaux
    print("\n1️⃣ Test API publique gâteaux:")
    try:
        response = requests.get('http://localhost:8000/api/public/gateaux/')
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
        response = requests.get('http://localhost:8000/api/parametres/')
        if response.status_code == 200:
            params = response.json()
            print(f"   ✅ {len(params)} paramètre(s) disponible(s)")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Création de commande
    print("\n3️⃣ Test création de commande:")
    try:
        data = {
            'gateau_id': gateau.id,
            'client_nom': 'Test Client',
            'client_telephone': '0123456789',
            'texte_sur_gateau': 'Test commande',
            'date_livraison': '2025-07-29T14:00:00',
            'livraison': True
        }
        
        response = requests.post('http://localhost:8000/api/commandes/create/', 
                               json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Commande créée avec succès!")
            print(f"   📋 ID: {result.get('commande_id')}")
            print(f"   💰 Prix total: {result.get('prix_total')} FCFA")
            
            # Vérifier le calcul
            prix_attendu = float(gateau.prix) + float(parametres.prix_livraison)
            print(f"   🧮 Prix attendu: {prix_attendu} FCFA")
            
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            print(f"   📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test final terminé!")
    print("\n📋 Résumé:")
    print(f"   - Gâteaux: {Gateau.objects.count()}")
    print(f"   - Paramètres: {ParametresLivraison.objects.count()}")
    print(f"   - Commandes: {Gateau.objects.count()}")

if __name__ == '__main__':
    test_final() 