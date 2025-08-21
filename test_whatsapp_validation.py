#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Commande, Gateau, ParametresLivraison

def test_whatsapp_validation():
    """Test de l'envoi automatique WhatsApp lors de la validation"""
    
    print("🎉 Test de l'envoi automatique WhatsApp lors de la validation:")
    print("=" * 60)
    
    # 1. Connexion patron
    print("\n1️⃣ Connexion patron:")
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
    
    # 2. Récupérer une commande en attente
    print("\n2️⃣ Récupération d'une commande en attente:")
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://localhost:8000/api/commandes/', headers=headers)
        
        if response.status_code == 200:
            commandes = response.json()
            commande_en_attente = None
            
            for cmd in commandes:
                if cmd['status'] == 'en_attente':
                    commande_en_attente = cmd
                    break
            
            if commande_en_attente:
                print(f"   ✅ Commande trouvée: #{commande_en_attente['id']}")
                print(f"   👤 Client: {commande_en_attente['client_nom']}")
                print(f"   📞 Téléphone: {commande_en_attente['client_telephone']}")
                print(f"   🎂 Gâteau: {commande_en_attente.get('gateau_nom', 'N/A')}")
            else:
                print("   ⚠️  Aucune commande en attente trouvée")
                return
        else:
            print(f"   ❌ Erreur: {response.status_code} - {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return
    
    # 3. Test de validation avec envoi WhatsApp automatique
    print("\n3️⃣ Test de validation avec envoi WhatsApp automatique:")
    try:
        # D'abord, valider la commande
        validation_response = requests.patch(
            f"http://localhost:8000/api/commandes/{commande_en_attente['id']}/",
            json={'status': 'validee'},
            headers=headers
        )
        
        if validation_response.status_code == 200:
            print(f"   ✅ Commande validée avec succès")
            
            # Ensuite, envoyer le message WhatsApp
            whatsapp_response = requests.post(
                f"http://localhost:8000/api/commandes/{commande_en_attente['id']}/send-whatsapp-validation/",
                headers=headers
            )
            
            if whatsapp_response.status_code == 200:
                result = whatsapp_response.json()
                print(f"   ✅ Message WhatsApp envoyé!")
                print(f"   📱 Lien WhatsApp: {result['whatsapp_link'][:50]}...")
                print(f"   👤 Client: {result['client_telephone']}")
                print(f"   📅 Date: {result['date_whatsapp']}")
                
                # Afficher le message généré
                print(f"\n📄 Message généré:")
                message_lines = result['whatsapp_link'].split('text=')[1].split('%0A')
                for line in message_lines:
                    if line:
                        print(f"   {line.replace('%20', ' ')}")
            else:
                print(f"   ❌ Erreur WhatsApp: {whatsapp_response.status_code} - {whatsapp_response.text}")
        else:
            print(f"   ❌ Erreur validation: {validation_response.status_code} - {validation_response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("   1. Aller sur http://localhost:3000/dashboard-patron")
    print("   2. Se connecter avec deliceDek@ty / delicedek@ty123")
    print("   3. Trouver une commande en attente")
    print("   4. Cliquer '✅ Valider'")
    print("   5. WhatsApp s'ouvrira automatiquement avec le message")

if __name__ == '__main__':
    test_whatsapp_validation() 