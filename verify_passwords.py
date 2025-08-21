#!/usr/bin/env python3
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User
from django.contrib.auth import authenticate

def verify_passwords():
    """Vérifier si les mots de passe ont été définis"""
    
    print("🔍 Vérification des mots de passe:")
    print("=" * 50)
    
    users = User.objects.all()
    
    for user in users:
        print(f"\n👤 Utilisateur: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Patron: {user.is_patron}")
        print(f"   - Collaborateur: {user.is_collaborateur}")
        print(f"   - Actif: {user.is_active}")
        print(f"   - Mot de passe défini: {user.has_usable_password()}")
        
        # Test avec le mot de passe attendu
        expected_password = f"{user.username.lower()}123"
        auth_user = authenticate(username=user.username, password=expected_password)
        
        if auth_user:
            print(f"   ✅ Authentification réussie avec: '{expected_password}'")
        else:
            print(f"   ❌ Authentification échouée avec: '{expected_password}'")
            
            # Test avec d'autres mots de passe possibles
            test_passwords = ['', 'password', '123456', user.username]
            for pwd in test_passwords:
                if authenticate(username=user.username, password=pwd):
                    print(f"   ✅ Authentification réussie avec: '{pwd}'")
                    break
            else:
                print(f"   ❌ Aucune authentification réussie")

if __name__ == '__main__':
    verify_passwords() 