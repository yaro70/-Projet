#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User
from django.contrib.auth import authenticate

def test_authentication():
    """Tester l'authentification des utilisateurs existants"""
    
    print("🔍 Test d'authentification des utilisateurs existants:")
    print("=" * 50)
    
    # Récupérer tous les utilisateurs
    users = User.objects.all()
    
    for user in users:
        print(f"\n👤 Utilisateur: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Patron: {user.is_patron}")
        print(f"   - Collaborateur: {user.is_collaborateur}")
        print(f"   - Actif: {user.is_active}")
        
        # Test d'authentification Django
        auth_user = authenticate(username=user.username, password='test123')
        if auth_user:
            print("   ✅ Authentification Django réussie avec 'test123'")
        else:
            print("   ❌ Authentification Django échouée avec 'test123'")
        
        # Test avec mot de passe vide
        auth_user_empty = authenticate(username=user.username, password='')
        if auth_user_empty:
            print("   ✅ Authentification Django réussie avec mot de passe vide")
        else:
            print("   ❌ Authentification Django échouée avec mot de passe vide")

def test_api_login():
    """Tester l'API de connexion"""
    
    print("\n🌐 Test de l'API de connexion:")
    print("=" * 50)
    
    # Test avec l'utilisateur YARO
    test_data = {
        'username': 'YARO',
        'password': 'test123'
    }
    
    try:
        response = requests.post('http://localhost:8000/api/login/', json=test_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur Django")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    test_authentication()
    test_api_login() 