#!/usr/bin/env python3
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User

def create_test_user():
    """Créer un utilisateur de test avec un mot de passe simple"""
    
    print("🔧 Création d'un utilisateur de test:")
    print("=" * 50)
    
    # Supprimer l'utilisateur de test s'il existe
    User.objects.filter(username='test').delete()
    
    # Créer un nouvel utilisateur de test
    test_user = User.objects.create_user(
        username='test',
        email='test@patisserie.com',
        password='test123',
        is_patron=True,
        is_collaborateur=False
    )
    
    print(f"✅ Utilisateur de test créé:")
    print(f"   - Username: {test_user.username}")
    print(f"   - Password: test123")
    print(f"   - Patron: {test_user.is_patron}")
    print(f"   - Collaborateur: {test_user.is_collaborateur}")
    
    # Vérifier l'authentification
    from django.contrib.auth import authenticate
    auth_user = authenticate(username='test', password='test123')
    
    if auth_user:
        print("   ✅ Authentification test réussie!")
    else:
        print("   ❌ Authentification test échouée!")
    
    print("\n🔑 Identifiants de test:")
    print("Username: test")
    print("Password: test123")

if __name__ == '__main__':
    create_test_user() 