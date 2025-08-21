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

def test_connection():
    """Tester la connexion avec les nouveaux mots de passe"""
    
    print("🔍 Test de connexion après définition des mots de passe:")
    print("=" * 60)
    
    # Test avec chaque utilisateur
    test_users = [
        ('YARO', 'yaro123'),
        ('deliceDek@ty', 'delicedek@ty123'),
        ('T0T01234', 't0t01234123')
    ]
    
    for username, password in test_users:
        print(f"\n👤 Test avec {username}:")
        
        # Test Django authenticate
        user = authenticate(username=username, password=password)
        if user:
            print(f"   ✅ Authentification Django réussie")
            print(f"   - Patron: {user.is_patron}")
            print(f"   - Collaborateur: {user.is_collaborateur}")
        else:
            print(f"   ❌ Authentification Django échouée")
        
        # Test API
        try:
            response = requests.post('http://localhost:8000/api/login/', 
                                  json={'username': username, 'password': password})
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ API connexion réussie")
                print(f"   - Token: {data.get('token', 'N/A')[:20]}...")
                print(f"   - User ID: {data.get('user_id')}")
            else:
                print(f"   ❌ API connexion échouée: {response.status_code}")
                print(f"   - Response: {response.text}")
        except requests.exceptions.ConnectionError:
            print("   ⚠️  Serveur Django non démarré")
        except Exception as e:
            print(f"   ❌ Erreur API: {e}")

if __name__ == '__main__':
    test_connection() 