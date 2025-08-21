#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau, Commande, User
from django.contrib.auth import authenticate

def test_dashboard_patron():
    """Test du dashboard patron"""
    
    print("👨‍🍳 Test du dashboard patron:")
    print("=" * 40)
    
    # 1. Test de connexion patron
    print("\n1️⃣ Test de connexion patron:")
    try:
        # Connexion avec un utilisateur patron
        login_data = {
            'username': 'deliceDek@ty',
            'password': 'delicedek@ty123'
        }
        
        response = requests.post('http://localhost:8000/api/login/', json=login_data)
        
        if response.status_code == 200:
            result = response.json()
            token = result['token']
            print(f"   ✅ Connexion réussie")
            print(f"   👤 Utilisateur: {result['username']}")
            print(f"   👑 Patron: {result['is_patron']}")
            print(f"   🔑 Token: {token[:20]}...")
        else:
            print(f"   ❌ Erreur de connexion: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return
    
    # 2. Test récupération des commandes
    print("\n2️⃣ Test récupération des commandes:")
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://localhost:8000/api/commandes/', headers=headers)
        
        if response.status_code == 200:
            commandes = response.json()
            print(f"   ✅ {len(commandes)} commande(s) récupérée(s)")
            
            for cmd in commandes:
                print(f"   📦 Commande #{cmd['id']}: {cmd['client_nom']} - {cmd.get('gateau_nom', 'N/A')} - {cmd['status']}")
        else:
            print(f"   ❌ Erreur: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Test mise à jour du statut d'une commande
    print("\n3️⃣ Test mise à jour du statut:")
    try:
        # Récupérer la première commande
        commandes = Commande.objects.all()
        if commandes.exists():
            commande = commandes.first()
            print(f"   📦 Test avec la commande #{commande.id}")
            
            # Mettre à jour le statut
            update_data = {'status': 'validee'}
            response = requests.patch(
                f'http://localhost:8000/api/commandes/{commande.id}/', 
                json=update_data, 
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"   ✅ Statut mis à jour avec succès")
                
                # Vérifier le changement
                updated_commande = Commande.objects.get(id=commande.id)
                print(f"   📊 Nouveau statut: {updated_commande.status}")
            else:
                print(f"   ❌ Erreur: {response.status_code} - {response.text}")
        else:
            print("   ⚠️  Aucune commande disponible pour le test")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test du dashboard patron terminé!")

if __name__ == '__main__':
    test_dashboard_patron() 