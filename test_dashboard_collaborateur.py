#!/usr/bin/env python3
"""
Test du dashboard collaborateur
"""

import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from django.contrib.auth import authenticate
from boutique.models import User, Commande, Gateau
from rest_framework.authtoken.models import Token
import requests
import json
from datetime import datetime, timedelta
from django.utils import timezone

def test_dashboard_collaborateur():
    """Test du dashboard collaborateur"""
    
    print("👨‍🍳 Test du dashboard collaborateur:")
    print("=" * 50)
    
    # 1. Connexion d'un collaborateur
    print("\n1️⃣ Connexion collaborateur:")
    collaborateur_username = "marie_dupont"  # Le collaborateur créé précédemment
    collaborateur_password = "marie123"
    
    try:
        # Authentification Django
        collaborateur = authenticate(username=collaborateur_username, password=collaborateur_password)
        if not collaborateur:
            print("❌ Échec de l'authentification Django")
            print("💡 Vérifiez que le collaborateur marie_dupont existe")
            return
        
        if not collaborateur.is_collaborateur:
            print("❌ L'utilisateur n'est pas un collaborateur")
            return
        
        print(f"✅ Connexion réussie")
        print(f"👤 Utilisateur: {collaborateur.username}")
        print(f"👨‍🍳 Rôle: Collaborateur")
        
        # Obtenir le token
        token, _ = Token.objects.get_or_create(user=collaborateur)
        print(f"🔑 Token: {token.key[:20]}...")
        
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return
    
    # 2. Vérifier les commandes disponibles
    print("\n2️⃣ Vérification des commandes disponibles:")
    total_commandes = Commande.objects.count()
    commandes_validees = Commande.objects.filter(status='validee').count()
    commandes_en_attente = Commande.objects.filter(status='en_attente').count()
    
    print(f"📦 Total commandes: {total_commandes}")
    print(f"✅ Commandes validées: {commandes_validees}")
    print(f"⏳ Commandes en attente: {commandes_en_attente}")
    
    # 3. Test de récupération des commandes via API (vue collaborateur)
    print("\n3️⃣ Test de récupération des commandes (vue collaborateur):")
    
    try:
        headers = {
            'Authorization': f'Token {token.key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'http://localhost:8000/api/commandes/',
            headers=headers
        )
        
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Commandes récupérées avec succès!")
            print(f"📦 Nombre de commandes reçues: {len(data)}")
            
            # Filtrer les commandes validées (comme le fait le frontend)
            commandes_validees_api = [cmd for cmd in data if cmd['status'] == 'validee']
            print(f"✅ Commandes validées dans la réponse: {len(commandes_validees_api)}")
            
            if commandes_validees_api:
                print("\n📋 Détails des commandes validées:")
                for cmd in commandes_validees_api:
                    print(f"  📦 Commande #{cmd['id']}:")
                    print(f"    👤 Client: {cmd['client_nom']}")
                    print(f"    📞 Téléphone: {cmd['client_telephone']}")
                    print(f"    🎂 Gâteau: {cmd.get('gateau_nom', cmd.get('gateau', 'N/A'))}")
                    print(f"    💰 Prix: {cmd['prix_total']} FCFA")
                    print(f"    📅 Date livraison: {cmd['date_livraison']}")
            else:
                print("ℹ️ Aucune commande validée disponible")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des commandes: {e}")
    
    # 4. Test de marquage comme terminée
    print("\n4️⃣ Test de marquage comme terminée:")
    
    # Trouver une commande validée
    commande_validee = Commande.objects.filter(status='validee').first()
    
    if commande_validee:
        print(f"🎯 Commande test: #{commande_validee.id} - {commande_validee.client_nom}")
        
        try:
            response = requests.post(
                f'http://localhost:8000/api/commandes/{commande_validee.id}/mark-terminee/',
                headers=headers
            )
            
            print(f"📥 Statut: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Commande marquée comme terminée avec succès!")
                print(f"📱 Lien WhatsApp: {data.get('whatsapp_link', 'N/A')[:50]}...")
                print(f"👤 Client: {data.get('client_telephone', 'N/A')}")
                print(f"🚚 Livraison: {data.get('livraison', 'N/A')}")
                
                # Vérifier en base de données
                commande_validee.refresh_from_db()
                print(f"✅ Vérification en base: statut = {commande_validee.status}")
                
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(f"📄 Réponse: {response.text}")
                
        except Exception as e:
            print(f"❌ Erreur lors du marquage: {e}")
    else:
        print("ℹ️ Aucune commande validée disponible pour le test")
    
    # 5. Test avec un utilisateur non-collaborateur
    print("\n5️⃣ Test avec un utilisateur non-collaborateur:")
    
    try:
        # Utiliser le patron pour le test
        patron = authenticate(username="deliceDek@ty", password="delicedek@ty123")
        if patron:
            patron_token, _ = Token.objects.get_or_create(user=patron)
            
            headers = {
                'Authorization': f'Token {patron_token.key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                'http://localhost:8000/api/commandes/',
                headers=headers
            )
            
            print(f"📥 Statut: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Patron peut voir toutes les commandes")
                print(f"📦 Nombre de commandes: {len(data)}")
            else:
                print(f"❌ Erreur pour le patron: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erreur lors du test patron: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("1. Aller sur http://localhost:3000/dashboard-collaborateur")
    print("2. Se connecter avec marie_dupont / marie123")
    print("3. Voir uniquement les commandes validées")
    print("4. Cliquer sur '🎂 Marquer comme terminé' pour terminer une commande")

if __name__ == "__main__":
    test_dashboard_collaborateur() 