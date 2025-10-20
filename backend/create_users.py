#!/usr/bin/env python3
"""
Script pour créer les utilisateurs de test
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from boutique.models import *

def create_test_users():
    """Crée les utilisateurs de test"""
    print("👤 Création des utilisateurs de test...")
    
    User = get_user_model()
    
    # Créer admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Admin créé: admin/admin123")
    else:
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')
        admin.save()
        print("✅ Admin mis à jour: admin/admin123")
    
    # Créer patron
    if not User.objects.filter(username='patron').exists():
        patron = User.objects.create_user(
            username='patron',
            email='patron@example.com',
            password='patron123',
            is_patron=True,
            is_staff=True
        )
        print("✅ Patron créé: patron/patron123")
    else:
        patron = User.objects.get(username='patron')
        patron.set_password('patron123')
        patron.is_patron = True
        patron.is_staff = True
        patron.save()
        print("✅ Patron mis à jour: patron/patron123")
    
    # Créer collaborateur
    if not User.objects.filter(username='collaborateur').exists():
        collaborateur = User.objects.create_user(
            username='collaborateur',
            email='collaborateur@example.com',
            password='collaborateur123',
            is_collaborateur=True
        )
        print("✅ Collaborateur créé: collaborateur/collaborateur123")
    else:
        collaborateur = User.objects.get(username='collaborateur')
        collaborateur.set_password('collaborateur123')
        collaborateur.is_collaborateur = True
        collaborateur.save()
        print("✅ Collaborateur mis à jour: collaborateur/collaborateur123")
    
    print("\n🔑 Identifiants de connexion :")
    print("=" * 50)
    print("| Rôle           | Username      | Password        |")
    print("|----------------|---------------|-----------------|")
    print("| Admin          | admin         | admin123        |")
    print("| Patron         | patron        | patron123       |")
    print("| Collaborateur  | collaborateur | collaborateur123|")
    print("=" * 50)

def create_test_data():
    """Crée les données de test"""
    print("\n📝 Création des données de test...")
    
    # Créer des gâteaux
    if Gateau.objects.count() == 0:
        from decimal import Decimal
        
        gateaux_data = [
            {
                'nom': 'Gâteau d\'Anniversaire Chocolat',
                'description': 'Délicieux gâteau au chocolat avec crème au beurre',
                'prix': Decimal('15000.00'),
                'type': 'anniversaire',
                'disponible': True
            },
            {
                'nom': 'Gâteau de Mariage Vanille',
                'description': 'Magnifique gâteau de mariage à la vanille',
                'prix': Decimal('25000.00'),
                'type': 'mariage',
                'disponible': True
            },
            {
                'nom': 'Cupcakes Assortis',
                'description': 'Assortiment de cupcakes aux saveurs variées',
                'prix': Decimal('8000.00'),
                'type': 'autre',
                'disponible': True
            }
        ]
        
        for data in gateaux_data:
            Gateau.objects.create(**data)
        
        print(f"✅ {len(gateaux_data)} gâteaux créés")
    
    # Créer des paramètres de livraison
    if ParametresLivraison.objects.count() == 0:
        from decimal import Decimal
        ParametresLivraison.objects.create(prix_livraison=Decimal('2000.00'))
        print("✅ Paramètres de livraison créés")

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
    print("🔧 Configuration des utilisateurs et données de test")
    print("=" * 60)
    
    try:
        create_test_users()
        create_test_data()
        test_authentication()
        
        print("\n🎉 Configuration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

