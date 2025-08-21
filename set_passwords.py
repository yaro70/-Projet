#!/usr/bin/env python3
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User

def set_passwords():
    """Définir des mots de passe pour les utilisateurs existants"""
    
    print("🔧 Définition des mots de passe:")
    print("=" * 50)
    
    users = User.objects.all()
    
    for user in users:
        # Définir un mot de passe simple basé sur le nom d'utilisateur
        new_password = f"{user.username.lower()}123"
        user.set_password(new_password)
        user.save()
        
        print(f"✅ {user.username}: mot de passe défini à '{new_password}'")
    
    print("\n🔑 Mots de passe définis:")
    print("YARO: yaro123")
    print("deliceDek@ty: delicedek@ty123")
    print("T0T01234: t0t01234123")
    print("\n💡 Vous pouvez maintenant vous connecter avec ces identifiants!")

if __name__ == '__main__':
    set_passwords() 