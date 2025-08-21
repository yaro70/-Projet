#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Commande, Gateau, ParametresLivraison

def test_terminaison_commande():
    """Test de la fonctionnalité de marquage des commandes comme terminées"""
    
    print("🎂 Test de la fonctionnalité de marquage des commandes comme terminées:")
    print("=" * 70)
    
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
    
    # 2. Récupérer une commande validée
    print("\n2️⃣ Récupération d'une commande validée:")
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://localhost:8000/api/commandes/', headers=headers)
        
        if response.status_code == 200:
            commandes = response.json()
            commande_validee = None
            
            for cmd in commandes:
                if cmd['status'] == 'validee':
                    commande_validee = cmd
                    break
            
            if commande_validee:
                print(f"   ✅ Commande trouvée: #{commande_validee['id']}")
                print(f"   👤 Client: {commande_validee['client_nom']}")
                print(f"   📞 Téléphone: {commande_validee['client_telephone']}")
                print(f"   🎂 Gâteau: {commande_validee.get('gateau_nom', 'N/A')}")
                print(f"   🚚 Livraison: {'Oui' if commande_validee['livraison'] else 'Non'}")
            else:
                print("   ⚠️  Aucune commande validée trouvée")
                return
        else:
            print(f"   ❌ Erreur: {response.status_code} - {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return
    
    # 3. Test de marquage comme terminée
    print("\n3️⃣ Test de marquage comme terminée:")
    try:
        response = requests.post(
            f"http://localhost:8000/api/commandes/{commande_validee['id']}/mark-terminee/",
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Commande marquée comme terminée!")
            print(f"   📱 Lien WhatsApp: {result['whatsapp_link'][:50]}...")
            print(f"   👤 Client: {result['client_telephone']}")
            print(f"   📅 Date: {result['date_whatsapp']}")
            print(f"   🚚 Livraison: {'Oui' if result['livraison'] else 'Non'}")
            
            # Afficher le message généré selon le type de livraison
            print(f"\n📄 Message généré ({'avec livraison' if result['livraison'] else 'sans livraison'}):")
            message_lines = result['whatsapp_link'].split('text=')[1].split('%0A')
            for line in message_lines:
                if line:
                    print(f"   {line.replace('%20', ' ')}")
        else:
            print(f"   ❌ Erreur: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("   1. Aller sur http://localhost:3000/dashboard-patron")
    print("   2. Se connecter avec deliceDek@ty / delicedek@ty123")
    print("   3. Trouver une commande validée")
    print("   4. Cliquer '🎂 Marquer terminé'")
    print("   5. WhatsApp s'ouvrira automatiquement avec le message approprié")

if __name__ == '__main__':
    test_terminaison_commande() 