#!/usr/bin/env python3
"""
Script pour corriger les identifiants de connexion
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from boutique.models import *

def fix_user_credentials():
    """Corrige les identifiants des utilisateurs"""
    print("🔧 Correction des identifiants de connexion...")
    
    User = get_user_model()
    
    # Identifiants par défaut
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin123',
            'is_superuser': True,
            'is_staff': True,
            'is_patron': False,
            'is_collaborateur': False
        },
        {
            'username': 'patron',
            'email': 'patron@example.com',
            'password': 'patron123',
            'is_superuser': False,
            'is_staff': True,
            'is_patron': True,
            'is_collaborateur': False
        },
        {
            'username': 'collaborateur',
            'email': 'collaborateur@example.com',
            'password': 'collaborateur123',
            'is_superuser': False,
            'is_staff': False,
            'is_patron': False,
            'is_collaborateur': True
        }
    ]
    
    for user_data in users_data:
        username = user_data['username']
        
        # Vérifier si l'utilisateur existe
        try:
            user = User.objects.get(username=username)
            print(f"✅ Utilisateur {username} existe déjà")
            
            # Mettre à jour le mot de passe
            user.set_password(user_data['password'])
            user.is_superuser = user_data['is_superuser']
            user.is_staff = user_data['is_staff']
            user.is_patron = user_data['is_patron']
            user.is_collaborateur = user_data['is_collaborateur']
            user.is_active = True
            user.save()
            
            print(f"✅ Mot de passe mis à jour pour {username}")
            
        except User.DoesNotExist:
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=username,
                email=user_data['email'],
                password=user_data['password'],
                is_superuser=user_data['is_superuser'],
                is_staff=user_data['is_staff'],
                is_patron=user_data['is_patron'],
                is_collaborateur=user_data['is_collaborateur'],
                is_active=True
            )
            print(f"✅ Utilisateur {username} créé")
    
    print("\n🔑 Identifiants de connexion :")
    print("=" * 50)
    print("| Rôle           | Username      | Password        |")
    print("|----------------|---------------|-----------------|")
    print("| Admin          | admin         | admin123        |")
    print("| Patron         | patron        | patron123       |")
    print("| Collaborateur  | collaborateur | collaborateur123|")
    print("=" * 50)

def check_database():
    """Vérifie l'état de la base de données"""
    print("\n🗄️ Vérification de la base de données...")
    
    User = get_user_model()
    
    # Compter les utilisateurs
    total_users = User.objects.count()
    print(f"📊 Total utilisateurs : {total_users}")
    
    # Lister tous les utilisateurs
    users = User.objects.all()
    for user in users:
        roles = []
        if user.is_superuser:
            roles.append("Superuser")
        if user.is_staff:
            roles.append("Staff")
        if user.is_patron:
            roles.append("Patron")
        if user.is_collaborateur:
            roles.append("Collaborateur")
        
        roles_str = ", ".join(roles) if roles else "Aucun rôle"
        print(f"👤 {user.username} - {roles_str} - Actif: {user.is_active}")
    
    # Vérifier les gâteaux
    gateaux_count = Gateau.objects.count()
    print(f"🎂 Total gâteaux : {gateaux_count}")
    
    # Vérifier les commandes
    commandes_count = Commande.objects.count()
    print(f"📦 Total commandes : {commandes_count}")

def test_authentication():
    """Teste l'authentification"""
    print("\n🧪 Test d'authentification...")
    
    from django.contrib.auth import authenticate
    
    test_credentials = [
        ('admin', 'admin123'),
        ('patron', 'patron123'),
        ('collaborateur', 'collaborateur123')
    ]
    
    for username, password in test_credentials:
        user = authenticate(username=username, password=password)
        if user:
            print(f"✅ {username} : Authentification réussie")
        else:
            print(f"❌ {username} : Échec d'authentification")

def main():
    """Fonction principale"""
    print("🔧 Script de correction des identifiants")
    print("=" * 50)
    
    try:
        # Corriger les identifiants
        fix_user_credentials()
        
        # Vérifier la base de données
        check_database()
        
        # Tester l'authentification
        test_authentication()
        
        print("\n🎉 Correction terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

