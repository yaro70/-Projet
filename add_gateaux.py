#!/usr/bin/env python3
import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau

def add_gateaux():
    """Ajouter des gâteaux de test"""
    
    print("🎂 Ajout de gâteaux de test:")
    print("=" * 50)
    
    # Supprimer les gâteaux existants pour éviter les doublons
    Gateau.objects.all().delete()
    print("🗑️  Anciens gâteaux supprimés")
    
    # Créer des gâteaux de test
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
        },
        {
            'nom': 'Gâteau au Citron',
            'type': 'autre',
            'description': 'Gâteau moelleux au citron avec glaçage acidulé',
            'prix': Decimal('12000.00'),
            'disponible': True
        },
        {
            'nom': 'Gâteau Red Velvet',
            'type': 'anniversaire',
            'description': 'Gâteau rouge velours avec crème au fromage',
            'prix': Decimal('18000.00'),
            'disponible': True
        }
    ]
    
    for gateau_data in gateaux_data:
        try:
            # Créer le gâteau sans image (le champ est maintenant optionnel)
            gateau = Gateau.objects.create(
                nom=gateau_data['nom'],
                type=gateau_data['type'],
                description=gateau_data['description'],
                prix=gateau_data['prix'],
                disponible=gateau_data['disponible']
            )
            print(f"   ✅ Gâteau créé: {gateau.nom} - {gateau.prix} FCFA")
        except Exception as e:
            print(f"   ❌ Erreur lors de la création de {gateau_data['nom']}: {e}")
    
    print(f"\n🎉 {Gateau.objects.count()} gâteaux créés avec succès!")

if __name__ == '__main__':
    add_gateaux() 