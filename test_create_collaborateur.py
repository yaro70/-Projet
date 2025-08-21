#!/usr/bin/env python3
"""
Test de création de collaborateurs
"""

import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from django.contrib.auth import authenticate
from boutique.models import User
from rest_framework.authtoken.models import Token
import requests
import json

def test_create_collaborateur():
    """Test de la création d'un collaborateur par un patron"""
    
    print("👥 Test de création de collaborateur:")
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
    
    # 2. Test de création de collaborateur via API
    print("\n2️⃣ Test de création de collaborateur via API:")
    
    collaborateur_data = {
        "nom": "Dupont",
        "prenom": "Marie",
        "telephone": "0123456789",
        "username": "marie_dupont",
        "password": "marie123"
    }
    
    try:
        headers = {
            'Authorization': f'Token {token.key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'http://localhost:8000/api/create-collaborateur/',
            json=collaborateur_data,
            headers=headers
        )
        
        print(f"📤 Données envoyées: {json.dumps(collaborateur_data, indent=2)}")
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Collaborateur créé avec succès!")
            print(f"👤 ID: {data['collaborateur']['id']}")
            print(f"👤 Username: {data['collaborateur']['username']}")
            print(f"👤 Nom: {data['collaborateur']['nom']}")
            print(f"👤 Prénom: {data['collaborateur']['prenom']}")
            print(f"📞 Téléphone: {data['collaborateur']['telephone']}")
            print(f"🔑 Token: {data['collaborateur']['token'][:20]}...")
            
            # Vérifier en base de données
            try:
                new_collaborateur = User.objects.get(username='marie_dupont')
                print(f"✅ Vérification en base: {new_collaborateur.username} (collaborateur: {new_collaborateur.is_collaborateur})")
            except User.DoesNotExist:
                print("❌ Collaborateur non trouvé en base de données")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
    
    # 3. Test avec un username existant
    print("\n3️⃣ Test avec un username existant:")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/create-collaborateur/',
            json=collaborateur_data,  # Même données
            headers=headers
        )
        
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Erreur attendue (username existe déjà)")
            print(f"📄 Message: {data.get('error', 'Erreur non spécifiée')}")
        else:
            print(f"❌ Comportement inattendu: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("1. Aller sur http://localhost:3000/dashboard-patron")
    print("2. Se connecter avec deliceDek@ty / delicedek@ty123")
    print("3. Aller dans la section '⚙️ Paramètres'")
    print("4. Cliquer sur 'Ajouter un collaborateur'")
    print("5. Remplir le formulaire et créer le collaborateur")

if __name__ == "__main__":
    test_create_collaborateur() 