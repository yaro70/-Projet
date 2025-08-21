#!/usr/bin/env python3
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User

def create_test_users():
    """Créer des utilisateurs de test avec différents rôles"""
    
    # Supprimer les utilisateurs existants pour éviter les conflits
    User.objects.filter(username__in=['admin', 'patron', 'collaborateur']).delete()
    
    # Créer un superutilisateur
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@patisserie.com',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )
    print(f"✅ Superutilisateur créé: {admin_user.username}")
    
    # Créer un patron
    patron_user = User.objects.create_user(
        username='patron',
        email='patron@patisserie.com',
        password='patron123',
        is_patron=True
    )
    print(f"✅ Patron créé: {patron_user.username}")
    
    # Créer un collaborateur
    collaborateur_user = User.objects.create_user(
        username='collaborateur',
        email='collaborateur@patisserie.com',
        password='collaborateur123',
        is_collaborateur=True
    )
    print(f"✅ Collaborateur créé: {collaborateur_user.username}")
    
    print("\n🔑 Identifiants de test:")
    print("Admin: admin / admin123")
    print("Patron: patron / patron123")
    print("Collaborateur: collaborateur / collaborateur123")

if __name__ == '__main__':
    create_test_users() 