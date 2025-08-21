#!/usr/bin/env python3
import os
import django
from decimal import Decimal, InvalidOperation

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau

def add_gateaux_fixed():
    """Ajouter des gâteaux de test avec gestion d'erreurs améliorée"""
    
    print("🎂 Ajout de gâteaux de test (version corrigée):")
    print("=" * 50)
    
    # Supprimer les gâteaux existants pour éviter les doublons
    Gateau.objects.all().delete()
    print("🗑️  Anciens gâteaux supprimés")
    
    # Créer des gâteaux de test avec gestion d'erreurs
    gateaux_data = [
        {
            'nom': 'Gâteau d\'Anniversaire Chocolat',
            'type': 'anniversaire',
            'description': 'Délicieux gâteau au chocolat avec crème chantilly et fruits rouges',
            'prix': '15000.00',
            'disponible': True
        },
        {
            'nom': 'Gâteau de Mariage Vanille',
            'type': 'mariage',
            'description': 'Élégant gâteau de mariage à la vanille avec décorations florales',
            'prix': '45000.00',
            'disponible': True
        },
        {
            'nom': 'Cupcakes Assortis',
            'type': 'autre',
            'description': 'Lot de 12 cupcakes avec différentes saveurs et décorations',
            'prix': '8000.00',
            'disponible': True
        },
        {
            'nom': 'Gâteau au Citron',
            'type': 'autre',
            'description': 'Gâteau moelleux au citron avec glaçage acidulé',
            'prix': '12000.00',
            'disponible': True
        },
        {
            'nom': 'Gâteau Red Velvet',
            'type': 'anniversaire',
            'description': 'Gâteau rouge velours avec crème au fromage',
            'prix': '18000.00',
            'disponible': True
        }
    ]
    
    succes_count = 0
    
    for gateau_data in gateaux_data:
        try:
            # Convertir le prix en Decimal de manière sécurisée
            prix_str = str(gateau_data['prix'])
            try:
                prix_decimal = Decimal(prix_str)
            except (InvalidOperation, ValueError) as e:
                print(f"   ❌ Prix invalide pour {gateau_data['nom']}: {prix_str} - {e}")
                continue
            
            # Créer le gâteau
            gateau = Gateau.objects.create(
                nom=gateau_data['nom'],
                type=gateau_data['type'],
                description=gateau_data['description'],
                prix=prix_decimal,
                disponible=gateau_data['disponible']
            )
            print(f"   ✅ Gâteau créé: {gateau.nom} - {gateau.prix} FCFA")
            succes_count += 1
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la création de {gateau_data['nom']}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 {succes_count} gâteaux créés avec succès!")
    
    # Vérifier le résultat
    gateaux_finaux = Gateau.objects.all()
    print(f"\n📊 Gâteaux en base de données:")
    for gateau in gateaux_finaux:
        print(f"   - {gateau.nom}: {gateau.prix} FCFA ({gateau.type})")

if __name__ == '__main__':
    add_gateaux_fixed() 