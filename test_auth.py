#!/usr/bin/env python3
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User
from django.contrib.auth import authenticate

def test_users():
    """Tester les utilisateurs existants"""
    
    print("🔍 Test des utilisateurs existants:")
    print("=" * 50)
    
    users = User.objects.all()
    
    for user in users:
        print(f"\n👤 Utilisateur: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Patron: {user.is_patron}")
        print(f"   - Collaborateur: {user.is_collaborateur}")
        print(f"   - Actif: {user.is_active}")
        print(f"   - Mot de passe défini: {user.has_usable_password()}")
        
        # Test avec différents mots de passe
        passwords_to_test = ['', 'test123', 'password', '123456', user.username]
        
        for password in passwords_to_test:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                print(f"   ✅ Authentification réussie avec: '{password}'")
                break
        else:
            print("   ❌ Aucune authentification réussie")

if __name__ == '__main__':
    test_users() 