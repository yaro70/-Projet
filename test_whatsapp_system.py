#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Commande, Gateau, ParametresLivraison

def test_whatsapp_system():
    """Test du système WhatsApp"""
    
    print("📱 Test du système WhatsApp:")
    print("=" * 40)
    
    # 1. Vérifier les commandes existantes
    print("\n1️⃣ Commandes existantes:")
    commandes = Commande.objects.all()
    print(f"   📊 Nombre de commandes: {commandes.count()}")
    
    for cmd in commandes:
        print(f"   📦 Commande #{cmd.id}: {cmd.client_nom}")
        print(f"      - WhatsApp envoyé: {cmd.whatsapp_envoye}")
        print(f"      - Date WhatsApp: {cmd.date_whatsapp}")
        print(f"      - Lien: {cmd.get_whatsapp_link()[:50]}...")
        print()
    
    # 2. Test de connexion patron
    print("\n2️⃣ Test de connexion patron:")
    try:
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
        else:
            print(f"   ❌ Erreur de connexion: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return
    
    # 3. Test récupération des commandes avec liens WhatsApp
    print("\n3️⃣ Test récupération des commandes:")
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://localhost:8000/api/commandes/', headers=headers)
        
        if response.status_code == 200:
            commandes_api = response.json()
            print(f"   ✅ {len(commandes_api)} commande(s) récupérée(s)")
            
            for cmd in commandes_api:
                print(f"   📦 Commande #{cmd['id']}: {cmd['client_nom']}")
                print(f"      - WhatsApp envoyé: {cmd.get('whatsapp_envoye', False)}")
                print(f"      - Lien WhatsApp: {cmd.get('whatsapp_link', 'N/A')[:50]}...")
        else:
            print(f"   ❌ Erreur: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 4. Test marquage WhatsApp envoyé
    print("\n4️⃣ Test marquage WhatsApp envoyé:")
    if commandes.exists():
        commande = commandes.first()
        print(f"   📦 Test avec la commande #{commande.id}")
        
        try:
            response = requests.post(
                f'http://localhost:8000/api/commandes/{commande.id}/mark-whatsapp/', 
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ WhatsApp marqué comme envoyé")
                print(f"   📊 Données: {result}")
                
                # Vérifier en base
                commande.refresh_from_db()
                print(f"   📱 WhatsApp envoyé: {commande.whatsapp_envoye}")
                print(f"   📅 Date: {commande.date_whatsapp}")
            else:
                print(f"   ❌ Erreur: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    else:
        print("   ⚠️  Aucune commande disponible pour le test")
    
    print("\n🎉 Test du système WhatsApp terminé!")

if __name__ == '__main__':
    test_whatsapp_system() 