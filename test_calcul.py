#!/usr/bin/env python3
import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau, ParametresLivraison

def test_calcul():
    """Test du calcul du prix total"""
    
    print("🧮 Test du calcul du prix total:")
    print("=" * 50)
    
    # Récupérer un gâteau de test
    gateau = Gateau.objects.first()
    if not gateau:
        print("❌ Aucun gâteau trouvé")
        return
    
    print(f"🎂 Gâteau: {gateau.nom}")
    print(f"   Prix: {gateau.prix} FCFA")
    print(f"   Type de prix: {type(gateau.prix)}")
    
    # Récupérer les paramètres de livraison
    parametres = ParametresLivraison.objects.first()
    if not parametres:
        print("❌ Aucun paramètre de livraison trouvé")
        return
    
    print(f"🚚 Frais de livraison: {parametres.prix_livraison} FCFA")
    print(f"   Type de frais: {type(parametres.prix_livraison)}")
    
    # Test du calcul
    print("\n🧮 Test du calcul:")
    
    # Méthode 1: Conversion explicite
    prix_gateau = Decimal(str(gateau.prix))
    frais_livraison = Decimal(str(parametres.prix_livraison))
    total_1 = prix_gateau + frais_livraison
    
    print(f"   Méthode 1 (Decimal): {prix_gateau} + {frais_livraison} = {total_1}")
    
    # Méthode 2: ParseFloat (comme dans le frontend)
    prix_gateau_float = float(gateau.prix)
    frais_livraison_float = float(parametres.prix_livraison)
    total_2 = prix_gateau_float + frais_livraison_float
    
    print(f"   Méthode 2 (Float): {prix_gateau_float} + {frais_livraison_float} = {total_2}")
    
    # Méthode 3: Concaténation (problème)
    prix_gateau_str = str(gateau.prix)
    frais_livraison_str = str(parametres.prix_livraison)
    total_3 = prix_gateau_str + frais_livraison_str
    
    print(f"   Méthode 3 (Concaténation): {prix_gateau_str} + {frais_livraison_str} = {total_3}")
    
    print(f"\n✅ Résultat correct: {total_1} FCFA")
    print(f"❌ Résultat incorrect: {total_3} FCFA")

if __name__ == '__main__':
    test_calcul() 