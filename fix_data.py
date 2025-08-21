#!/usr/bin/env python3
import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User, Gateau, Commande, ParametresLivraison

def fix_data():
    """Corriger les données existantes"""
    
    print("🔧 Correction des données:")
    print("=" * 50)
    
    # 1. Corriger les paramètres de livraison
    print("📝 Correction des paramètres de livraison...")
    parametres = ParametresLivraison.objects.all()
    for param in parametres:
        if not isinstance(param.prix_livraison, Decimal):
            param.prix_livraison = Decimal(str(param.prix_livraison))
            param.save()
            print(f"   ✅ Prix corrigé: {param.prix_livraison}")
    
    # 2. Corriger les prix des gâteaux
    print("📝 Correction des prix des gâteaux...")
    gateaux = Gateau.objects.all()
    for gateau in gateaux:
        if not isinstance(gateau.prix, Decimal):
            gateau.prix = Decimal(str(gateau.prix))
            gateau.save()
            print(f"   ✅ Prix corrigé pour {gateau.nom}: {gateau.prix}")
    
    # 3. Corriger les prix des commandes
    print("📝 Correction des prix des commandes...")
    commandes = Commande.objects.all()
    for cmd in commandes:
        if not isinstance(cmd.prix_total, Decimal):
            cmd.prix_total = Decimal(str(cmd.prix_total))
            cmd.save()
            print(f"   ✅ Prix corrigé pour commande #{cmd.id}: {cmd.prix_total}")
    
    # 4. Créer des données de test si nécessaire
    if Gateau.objects.count() == 0:
        print("📝 Création de gâteaux de test...")
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
    
    if ParametresLivraison.objects.count() == 0:
        print("📝 Création des paramètres de livraison...")
        ParametresLivraison.objects.create(prix_livraison=Decimal('2000.00'))
        print("   ✅ Paramètres de livraison créés")
    
    # 5. Définir les mots de passe
    print("🔑 Définition des mots de passe...")
    users = User.objects.all()
    for user in users:
        if not user.has_usable_password():
            new_password = f"{user.username.lower()}123"
            user.set_password(new_password)
            user.save()
            print(f"   ✅ Mot de passe défini pour {user.username}: {new_password}")
    
    print("\n🎉 Correction terminée!")
    print("\n📋 Résumé:")
    print(f"   - {Gateau.objects.count()} gâteaux")
    print(f"   - {ParametresLivraison.objects.count()} paramètre(s)")
    print(f"   - {Commande.objects.count()} commande(s)")
    print(f"   - {users.count()} utilisateur(s)")

if __name__ == '__main__':
    fix_data() 