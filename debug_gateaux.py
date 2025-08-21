#!/usr/bin/env python3
import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau

def debug_gateaux():
    """Diagnostic des problèmes avec les gâteaux"""
    
    print("🔍 Diagnostic des gâteaux:")
    print("=" * 50)
    
    # Vérifier le modèle
    print("\n1️⃣ Vérification du modèle Gateau:")
    gateau_fields = Gateau._meta.get_fields()
    for field in gateau_fields:
        if field.name == 'prix':
            print(f"   - Champ 'prix': {field.__class__.__name__}")
            print(f"     max_digits: {field.max_digits}")
            print(f"     decimal_places: {field.decimal_places}")
            print(f"     null: {field.null}")
            print(f"     blank: {field.blank}")
    
    # Tester la création d'un gâteau simple
    print("\n2️⃣ Test de création d'un gâteau simple:")
    try:
        # Supprimer tous les gâteaux existants
        Gateau.objects.all().delete()
        print("   ✅ Gâteaux existants supprimés")
        
        # Créer un gâteau de test
        gateau_test = Gateau.objects.create(
            nom='Test Gateau',
            type='autre',
            description='Test description',
            prix=Decimal('1000.00'),
            disponible=True
        )
        print(f"   ✅ Gâteau de test créé: {gateau_test.nom} - {gateau_test.prix}")
        
        # Vérifier les gâteaux existants
        gateaux = Gateau.objects.all()
        print(f"   📊 Nombre de gâteaux en base: {gateaux.count()}")
        
        for gateau in gateaux:
            print(f"      - {gateau.nom}: {gateau.prix} ({type(gateau.prix)})")
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
    
    # Test avec différents formats de prix
    print("\n3️⃣ Test avec différents formats de prix:")
    test_prix = [
        Decimal('1000.00'),
        Decimal('15000.00'),
        Decimal('45000.00'),
        Decimal('8000.00'),
        Decimal('12000.00'),
        Decimal('18000.00')
    ]
    
    for i, prix in enumerate(test_prix):
        try:
            gateau = Gateau.objects.create(
                nom=f'Test Gateau {i+1}',
                type='autre',
                description=f'Test description {i+1}',
                prix=prix,
                disponible=True
            )
            print(f"   ✅ Prix {prix}: OK")
        except Exception as e:
            print(f"   ❌ Prix {prix}: {e}")
    
    print(f"\n📊 Total gâteaux en base: {Gateau.objects.count()}")

if __name__ == '__main__':
    debug_gateaux() 