#!/usr/bin/env python3
"""
Test du système de notifications en temps réel
"""

import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User, Commande, Notification
import requests
import json
import time

def test_notifications():
    """Test du système de notifications"""
    
    print("🔔 Test du système de notifications en temps réel:")
    print("=" * 60)
    
    # 1. Vérifier les utilisateurs patrons
    print("\n1️⃣ Vérification des utilisateurs patrons:")
    patrons = User.objects.filter(is_patron=True)
    print(f"👑 Patrons trouvés: {patrons.count()}")
    
    for patron in patrons:
        print(f"  👤 {patron.username} ({patron.first_name} {patron.last_name})")
    
    if not patrons.exists():
        print("❌ Aucun patron trouvé - impossible de tester les notifications")
        return
    
    patron = patrons.first()
    
    # 2. Connexion du patron
    print(f"\n2️⃣ Connexion du patron {patron.username}:")
    
    try:
        login_data = {
            'username': patron.username,
            'password': 'delicedek@ty123' if patron.username == 'deliceDek@ty' else 't0t01234123'
        }
        
        response = requests.post('http://localhost:8000/api/login/', data=login_data)
        
        if response.status_code == 200:
            token = response.json()['token']
            print(f"✅ Connexion réussie")
            print(f"🔑 Token: {token[:20]}...")
        else:
            print(f"❌ Échec de connexion: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # 3. Test de récupération des notifications
    print(f"\n3️⃣ Test de récupération des notifications:")
    
    try:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://localhost:8000/api/notifications/', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Notifications récupérées avec succès")
            print(f"📰 Total notifications: {len(data['notifications'])}")
            print(f"📬 Non lues: {data['unread_count']}")
            
            if data['notifications']:
                print("\n📋 Dernières notifications:")
                for notif in data['notifications'][:3]:
                    print(f"  📰 {notif['title']} ({notif['type']})")
                    print(f"    📝 {notif['message'][:50]}...")
                    print(f"    📅 {notif['created_at']}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération: {e}")
    
    # 4. Test de création d'une commande (déclenche notification)
    print(f"\n4️⃣ Test de création d'une commande (déclenche notification):")
    
    try:
        # Récupérer un gâteau disponible
        gateaux_response = requests.get('http://localhost:8000/api/public/gateaux/')
        if gateaux_response.status_code == 200:
            gateaux = gateaux_response.json()
            if gateaux:
                gateau = gateaux[0]
                print(f"🎂 Gâteau sélectionné: {gateau['nom']}")
                
                # Créer une commande
                commande_data = {
                    'gateau_id': gateau['id'],
                    'client_nom': 'Test Client Notifications',
                    'client_telephone': '0123456789',
                    'texte_sur_gateau': 'Test notifications',
                    'date_livraison': '2025-07-30T15:00',
                    'livraison': True
                }
                
                response = requests.post('http://localhost:8000/api/create-commande/', json=commande_data)
                
                if response.status_code == 201:
                    commande_info = response.json()
                    print(f"✅ Commande créée: #{commande_info['commande_id']}")
                    print(f"💰 Prix total: {commande_info['prix_total']} FCFA")
                    
                    # Attendre un peu pour que la notification soit créée
                    print("⏳ Attente de la création de la notification...")
                    time.sleep(2)
                    
                    # Vérifier les nouvelles notifications
                    response = requests.get('http://localhost:8000/api/notifications/', headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"📰 Nouvelles notifications: {len(data['notifications'])}")
                        print(f"📬 Non lues: {data['unread_count']}")
                        
                        # Chercher la notification de nouvelle commande
                        new_order_notifications = [
                            n for n in data['notifications'] 
                            if n['type'] == 'new_order' and 'Test Client Notifications' in n['message']
                        ]
                        
                        if new_order_notifications:
                            notif = new_order_notifications[0]
                            print(f"✅ Notification de nouvelle commande trouvée!")
                            print(f"📰 Titre: {notif['title']}")
                            print(f"📝 Message: {notif['message']}")
                            print(f"📊 Données: {notif['data']}")
                        else:
                            print("❌ Notification de nouvelle commande non trouvée")
                    else:
                        print(f"❌ Erreur lors de la vérification: {response.status_code}")
                else:
                    print(f"❌ Erreur lors de la création: {response.status_code}")
                    print(f"📄 Réponse: {response.text}")
            else:
                print("❌ Aucun gâteau disponible")
        else:
            print(f"❌ Erreur lors de la récupération des gâteaux: {gateaux_response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de commande: {e}")
    
    # 5. Test de marquage comme lu
    print(f"\n5️⃣ Test de marquage comme lu:")
    
    try:
        # Récupérer les notifications non lues
        response = requests.get('http://localhost:8000/api/notifications/', headers=headers)
        if response.status_code == 200:
            data = response.json()
            unread_notifications = [n for n in data['notifications'] if not n['is_read']]
            
            if unread_notifications:
                notif_to_mark = unread_notifications[0]
                print(f"📰 Marquage de la notification #{notif_to_mark['id']} comme lue")
                
                mark_response = requests.post(
                    'http://localhost:8000/api/notifications/mark-read/',
                    json={'notification_id': notif_to_mark['id']},
                    headers=headers
                )
                
                if mark_response.status_code == 200:
                    print("✅ Notification marquée comme lue")
                    
                    # Vérifier le changement
                    response = requests.get('http://localhost:8000/api/notifications/', headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        updated_notif = next((n for n in data['notifications'] if n['id'] == notif_to_mark['id']), None)
                        if updated_notif and updated_notif['is_read']:
                            print("✅ Vérification: notification bien marquée comme lue")
                        else:
                            print("❌ Vérification échouée: notification toujours non lue")
                    else:
                        print(f"❌ Erreur lors de la vérification: {response.status_code}")
                else:
                    print(f"❌ Erreur lors du marquage: {mark_response.status_code}")
            else:
                print("ℹ️ Aucune notification non lue à marquer")
        else:
            print(f"❌ Erreur lors de la récupération: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de marquage: {e}")
    
    # 6. Test de marquage de toutes comme lues
    print(f"\n6️⃣ Test de marquage de toutes comme lues:")
    
    try:
        response = requests.post('http://localhost:8000/api/notifications/mark-all-read/', headers=headers)
        
        if response.status_code == 200:
            print("✅ Toutes les notifications marquées comme lues")
            
            # Vérifier
            response = requests.get('http://localhost:8000/api/notifications/', headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"📬 Non lues après marquage: {data['unread_count']}")
            else:
                print(f"❌ Erreur lors de la vérification: {response.status_code}")
        else:
            print(f"❌ Erreur lors du marquage: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de marquage global: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("1. Aller sur http://localhost:3000/dashboard-patron")
    print("2. Se connecter avec un compte patron")
    print("3. Voir l'icône de notifications dans l'en-tête")
    print("4. Créer une commande depuis la page d'accueil")
    print("5. Vérifier que la notification apparaît en temps réel")
    print("6. Tester les WebSockets en ouvrant plusieurs onglets")

if __name__ == "__main__":
    test_notifications() 