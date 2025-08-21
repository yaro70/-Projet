#!/usr/bin/env python3
"""
Test de l'organisation des commandes en sections
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

def test_sections_commandes():
    """Test de l'organisation des commandes en sections"""
    
    print("📦 Test de l'organisation des commandes en sections:")
    print("=" * 60)
    
    # 1. Vérifier l'état actuel des commandes
    print("\n1️⃣ État actuel des commandes:")
    total_commandes = Commande.objects.count()
    commandes_en_attente = Commande.objects.filter(status='en_attente').count()
    commandes_validees = Commande.objects.filter(status='validee').count()
    commandes_terminees = Commande.objects.filter(status='terminee').count()
    commandes_refusees = Commande.objects.filter(status='refusee').count()
    
    print(f"📦 Total commandes: {total_commandes}")
    print(f"⏳ En attente: {commandes_en_attente}")
    print(f"✅ Validées: {commandes_validees}")
    print(f"🎂 Terminées: {commandes_terminees}")
    print(f"❌ Refusées: {commandes_refusees}")
    
    # 2. Test vue patron
    print("\n2️⃣ Test vue patron (toutes les commandes):")
    
    try:
        patron = authenticate(username="deliceDek@ty", password="delicedek@ty123")
        if not patron:
            print("❌ Échec de l'authentification patron")
            return
        
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
            print("✅ Commandes récupérées avec succès!")
            
            # Analyser les sections
            sections = {
                'en_attente': [cmd for cmd in data if cmd['status'] == 'en_attente'],
                'validee': [cmd for cmd in data if cmd['status'] == 'validee'],
                'terminee': [cmd for cmd in data if cmd['status'] == 'terminee'],
                'refusee': [cmd for cmd in data if cmd['status'] == 'refusee']
            }
            
            print("\n📊 Répartition par section (vue patron):")
            for section, commandes in sections.items():
                section_name = {
                    'en_attente': '⏳ En attente',
                    'validee': '✅ Validées',
                    'terminee': '🎂 Terminées',
                    'refusee': '❌ Refusées'
                }.get(section, section)
                print(f"  {section_name}: {len(commandes)} commande(s)")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test patron: {e}")
    
    # 3. Test vue collaborateur
    print("\n3️⃣ Test vue collaborateur (commandes non terminées):")
    
    try:
        collaborateur = authenticate(username="marie_dupont", password="marie123")
        if not collaborateur:
            print("❌ Échec de l'authentification collaborateur")
            return
        
        collab_token, _ = Token.objects.get_or_create(user=collaborateur)
        
        headers = {
            'Authorization': f'Token {collab_token.key}',
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
            
            # Analyser les sections (collaborateur ne voit que les non terminées)
            sections_collab = {
                'en_attente': [cmd for cmd in data if cmd['status'] == 'en_attente'],
                'validee': [cmd for cmd in data if cmd['status'] == 'validee'],
                'refusee': [cmd for cmd in data if cmd['status'] == 'refusee']
            }
            
            print("\n📊 Répartition par section (vue collaborateur):")
            for section, commandes in sections_collab.items():
                section_name = {
                    'en_attente': '⏳ En attente',
                    'validee': '✅ Validées',
                    'refusee': '❌ Refusées'
                }.get(section, section)
                print(f"  {section_name}: {len(commandes)} commande(s)")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test collaborateur: {e}")
    
    # 4. Test de création d'une nouvelle commande
    print("\n4️⃣ Test de création d'une nouvelle commande:")
    
    try:
        # Créer une nouvelle commande
        gateau = Gateau.objects.first()
        if gateau:
            nouvelle_commande = Commande.objects.create(
                client_nom="Test Client Section",
                client_telephone="0123456789",
                gateau=gateau,
                texte_sur_gateau="Test section",
                date_livraison=timezone.now() + timedelta(days=1),
                livraison=True,
                prix_total=gateau.prix + 2000,  # Prix + livraison
                status='en_attente'
            )
            
            print(f"✅ Nouvelle commande créée: #{nouvelle_commande.id}")
            print(f"📦 Statut: {nouvelle_commande.status}")
            print(f"👤 Client: {nouvelle_commande.client_nom}")
            
            # Vérifier qu'elle apparaît dans la bonne section
            print("\n📊 Vérification des sections après création:")
            total_apres = Commande.objects.count()
            en_attente_apres = Commande.objects.filter(status='en_attente').count()
            
            print(f"📦 Total commandes: {total_apres}")
            print(f"⏳ En attente: {en_attente_apres}")
            
        else:
            print("❌ Aucun gâteau disponible pour créer une commande")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("1. Aller sur http://localhost:3000/dashboard-patron")
    print("2. Se connecter avec deliceDek@ty / delicedek@ty123")
    print("3. Voir les commandes organisées en sections:")
    print("   - ⏳ Commandes en attente")
    print("   - ✅ Commandes validées")
    print("   - 🎂 Commandes terminées")
    print("   - ❌ Commandes refusées")
    print("4. Aller sur http://localhost:3000/dashboard-collaborateur")
    print("5. Se connecter avec marie_dupont / marie123")
    print("6. Voir les commandes organisées en sections:")
    print("   - ✅ Commandes validées à traiter")
    print("   - 🎂 Commandes terminées")

if __name__ == "__main__":
    test_sections_commandes() 