#!/usr/bin/env python3
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User, Gateau, ParametresLivraison

def fix_permissions():
    """Corriger les permissions et créer les données de base"""
    
    print("🔧 Correction des permissions et données:")
    print("=" * 50)
    
    # 1. Créer les données de test si elles n'existent pas
    if Gateau.objects.count() == 0:
        print("📝 Création des gâteaux de test...")
        from decimal import Decimal
        
        gateaux_data = [
            {
                'nom': 'Gâteau d\'Anniversaire Chocolat',
                'type': 'anniversaire',
                'description': 'Délicieux gâteau au chocolat avec crème chantilly et fruits rouges',
                'prix': Decimal('15000.00'),
                'disponible': True
            },
            {
                'nom': 'Gâteau de Mariage Vanille',
                'type': 'mariage',
                'description': 'Élégant gâteau de mariage à la vanille avec décorations florales',
                'prix': Decimal('45000.00'),
                'disponible': True
            },
            {
                'nom': 'Cupcakes Assortis',
                'type': 'autre',
                'description': 'Lot de 12 cupcakes avec différentes saveurs et décorations',
                'prix': Decimal('8000.00'),
                'disponible': True
            }
        ]
        
        for gateau_data in gateaux_data:
            Gateau.objects.create(**gateau_data)
            print(f"   ✅ Gâteau créé: {gateau_data['nom']}")
    
    # 2. Créer les paramètres de livraison si ils n'existent pas
    if ParametresLivraison.objects.count() == 0:
        print("📝 Création des paramètres de livraison...")
        from decimal import Decimal
        ParametresLivraison.objects.create(prix_livraison=Decimal('2000.00'))
        print("   ✅ Paramètres de livraison créés")
    
    # 3. Vérifier les utilisateurs
    print("👥 Vérification des utilisateurs:")
    users = User.objects.all()
    for user in users:
        print(f"   - {user.username}: Patron={user.is_patron}, Collaborateur={user.is_collaborateur}")
    
    # 4. Définir les mots de passe si nécessaire
    print("🔑 Définition des mots de passe...")
    for user in users:
        if not user.has_usable_password():
            new_password = f"{user.username.lower()}123"
            user.set_password(new_password)
            user.save()
            print(f"   ✅ Mot de passe défini pour {user.username}: {new_password}")
    
    print("\n🎉 Configuration terminée!")
    print("\n📋 Résumé:")
    print(f"   - {Gateau.objects.count()} gâteaux disponibles")
    print(f"   - {ParametresLivraison.objects.count()} paramètre(s) de livraison")
    print(f"   - {users.count()} utilisateur(s)")
    
    print("\n🔑 Identifiants de test:")
    for user in users:
        print(f"   - {user.username}: {user.username.lower()}123")

if __name__ == '__main__':
    fix_permissions() 