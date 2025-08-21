#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau, ParametresLivraison

def test_commande():
    """Test de création de commande"""
    
    print("🧪 Test de création de commande:")
    print("=" * 50)
    
    # Vérifier les données disponibles
    gateau = Gateau.objects.first()
    if not gateau:
        print("❌ Aucun gâteau trouvé")
        return
    
    parametres = ParametresLivraison.objects.first()
    if not parametres:
        print("❌ Aucun paramètre de livraison trouvé")
        return
    
    print(f"🎂 Gâteau: {gateau.nom} - {gateau.prix} FCFA")
    print(f"🚚 Livraison: {parametres.prix_livraison} FCFA")
    
    # Test de l'API
    try:
        # Données de test
        data = {
            'gateau_id': gateau.id,
            'client_nom': 'Test Client',
            'client_telephone': '0123456789',
            'texte_sur_gateau': 'Test commande',
            'date_livraison': '2025-07-29T14:00:00',
            'livraison': True
        }
        
        print(f"\n📤 Envoi de la commande...")
        response = requests.post('http://localhost:8000/api/commandes/create/', 
                               json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Commande créée avec succès!")
            print(f"   ID: {result.get('commande_id')}")
            print(f"   Prix total: {result.get('prix_total')} FCFA")
            
            # Vérifier le calcul
            prix_attendu = float(gateau.prix) + float(parametres.prix_livraison)
            print(f"   Prix attendu: {prix_attendu} FCFA")
            
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Réponse: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur Django")
        print("   Assurez-vous que le serveur est démarré: python manage.py runserver 8000")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    test_commande() 