#!/usr/bin/env python3
"""
Test des statistiques du dashboard patron
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

def test_statistiques():
    """Test des statistiques du dashboard patron"""
    
    print("📊 Test des statistiques:")
    print("=" * 50)
    
    # 1. Connexion d'un patron
    print("\n1️⃣ Connexion patron:")
    patron_username = "deliceDek@ty"
    patron_password = "delicedek@ty123"
    
    try:
        # Authentification Django
        patron = authenticate(username=patron_username, password=patron_password)
        if not patron:
            print("❌ Échec de l'authentification Django")
            return
        
        if not patron.is_patron:
            print("❌ L'utilisateur n'est pas un patron")
            return
        
        print(f"✅ Connexion réussie")
        print(f"👤 Utilisateur: {patron.username}")
        print(f"👑 Rôle: Patron")
        
        # Obtenir le token
        token, _ = Token.objects.get_or_create(user=patron)
        print(f"🔑 Token: {token.key[:20]}...")
        
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return
    
    # 2. Vérifier les données existantes
    print("\n2️⃣ Vérification des données existantes:")
    total_commandes = Commande.objects.count()
    total_gateaux = Gateau.objects.count()
    print(f"📦 Total commandes: {total_commandes}")
    print(f"🎂 Total gâteaux: {total_gateaux}")
    
    # 3. Test des statistiques via API
    print("\n3️⃣ Test des statistiques via API:")
    
    try:
        headers = {
            'Authorization': f'Token {token.key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'http://localhost:8000/api/statistiques/',
            headers=headers
        )
        
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Statistiques récupérées avec succès!")
            
            # Afficher les statistiques par période
            print("\n📈 Statistiques par période:")
            for periode, stats in data['statistiques_periode'].items():
                print(f"  📅 {periode.capitalize()}:")
                print(f"    📦 Commandes: {stats['commandes']}")
                print(f"    💰 Chiffre d'affaires: {stats['chiffre_affaires']:,.0f} FCFA")
                print(f"    📊 Période: {data['periode_calcul'][periode]}")
            
            # Afficher les statistiques par statut
            print("\n📊 Répartition par statut:")
            for status, count in data['statistiques_status'].items():
                status_name = {
                    'en_attente': '⏳ En attente',
                    'validee': '✅ Validées',
                    'refusee': '❌ Refusées',
                    'terminee': '🎂 Terminées'
                }.get(status, status)
                print(f"  {status_name}: {count}")
            
            # Afficher le top gâteaux
            print("\n🏆 Top gâteaux:")
            if data['top_gateaux']:
                for i, gateau in enumerate(data['top_gateaux'], 1):
                    print(f"  #{i} {gateau['gateau__nom']}: {gateau['total_commandes']} commandes")
            else:
                print("  Aucun gâteau commandé")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des statistiques: {e}")
    
    # 4. Test avec un utilisateur non-patron
    print("\n4️⃣ Test avec un utilisateur non-patron:")
    
    try:
        # Créer un utilisateur collaborateur pour le test
        collaborateur, created = User.objects.get_or_create(
            username='test_collab_stats',
            defaults={
                'first_name': 'Test',
                'last_name': 'Collaborateur',
                'is_collaborateur': True,
                'is_patron': False
            }
        )
        if created:
            collaborateur.set_password('test123')
            collaborateur.save()
            print(f"👤 Collaborateur de test créé: {collaborateur.username}")
        
        # Obtenir le token du collaborateur
        collab_token, _ = Token.objects.get_or_create(user=collaborateur)
        
        headers = {
            'Authorization': f'Token {collab_token.key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'http://localhost:8000/api/statistiques/',
            headers=headers
        )
        
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 403:
            print("✅ Accès refusé correctement (seuls les patrons peuvent voir les statistiques)")
        else:
            print(f"❌ Comportement inattendu: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'accès: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("1. Aller sur http://localhost:3000/dashboard-patron")
    print("2. Se connecter avec deliceDek@ty / delicedek@ty123")
    print("3. Cliquer sur '📊 Statistiques' dans la sidebar")
    print("4. Voir les statistiques par période, statut et top gâteaux")

if __name__ == "__main__":
    test_statistiques() 