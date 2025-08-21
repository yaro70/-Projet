#!/usr/bin/env python3
import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau, ParametresLivraison

def create_test_data_simple():
    """Créer des données de test simples sans images"""
    
    print("🔧 Création des données de test (version simple):")
    print("=" * 50)
    
    # Supprimer les données existantes
    Gateau.objects.all().delete()
    ParametresLivraison.objects.all().delete()
    
    # Créer des gâteaux de test (sans images)
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
        # Créer le gâteau sans image
        gateau = Gateau.objects.create(
            nom=gateau_data['nom'],
            type=gateau_data['type'],
            description=gateau_data['description'],
            prix=gateau_data['prix'],
            disponible=gateau_data['disponible']
        )
        print(f"✅ Gâteau créé: {gateau.nom} - {gateau.prix} FCFA")
    
    # Créer les paramètres de livraison
    parametres = ParametresLivraison.objects.create(prix_livraison=Decimal('2000.00'))
    print(f"✅ Paramètres de livraison créés: {parametres.prix_livraison} FCFA")
    
    print("\n🎂 Gâteaux disponibles:")
    for gateau in Gateau.objects.all():
        print(f"   - {gateau.nom}: {gateau.prix} FCFA")
    
    print(f"\n🚚 Prix de livraison: {parametres.prix_livraison} FCFA")

if __name__ == '__main__':
    create_test_data_simple() 