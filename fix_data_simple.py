#!/usr/bin/env python3
import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User, Gateau, Commande, ParametresLivraison

def fix_data_simple():
    """Corriger les données existantes sans créer de nouveaux gâteaux"""
    
    print("🔧 Correction des données (version simple):")
    print("=" * 50)
    
    # 1. Corriger les paramètres de livraison
    print("📝 Correction des paramètres de livraison...")
    parametres = ParametresLivraison.objects.all()
    for param in parametres:
        if not isinstance(param.prix_livraison, Decimal):
            param.prix_livraison = Decimal(str(param.prix_livraison))
            param.save()
            print(f"   ✅ Prix corrigé: {param.prix_livraison}")
    
    # 2. Corriger les prix des gâteaux existants
    print("📝 Correction des prix des gâteaux existants...")
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
    
    # 4. Créer les paramètres de livraison si ils n'existent pas
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
    
    print("\n🔑 Identifiants de test:")
    for user in users:
        print(f"   - {user.username}: {user.username.lower()}123")

if __name__ == '__main__':
    fix_data_simple() 