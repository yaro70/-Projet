#!/usr/bin/env python3
"""
Script pour mettre à jour les paramètres existants avec le numéro du patron
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import ParametresLivraison

def update_parametres():
    """Mettre à jour les paramètres existants avec le numéro du patron"""
    print("📞 MISE À JOUR DES PARAMÈTRES")
    print("=" * 50)
    
    try:
        # Récupérer ou créer les paramètres
        parametres, created = ParametresLivraison.objects.get_or_create(
            defaults={
                'prix_livraison': 2000.00,
                'numero_patron': '2250123456789'
            }
        )
        
        if created:
            print("✅ Nouveaux paramètres créés:")
            print(f"   Prix livraison: {parametres.prix_livraison} FCFA")
            print(f"   Numéro patron: {parametres.numero_patron}")
        else:
            # Mettre à jour le numéro si ce n'est pas défini
            if not parametres.numero_patron or parametres.numero_patron == '':
                parametres.numero_patron = '2250123456789'
                parametres.save()
                print("✅ Numéro du patron mis à jour:")
                print(f"   Prix livraison: {parametres.prix_livraison} FCFA")
                print(f"   Numéro patron: {parametres.numero_patron}")
            else:
                print("✅ Paramètres déjà configurés:")
                print(f"   Prix livraison: {parametres.prix_livraison} FCFA")
                print(f"   Numéro patron: {parametres.numero_patron}")
        
        print("\n🎉 MISE À JOUR TERMINÉE!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

def main():
    """Fonction principale"""
    print("📞 CONFIGURATION DU NUMÉRO PATRON")
    print("=" * 50)
    
    success = update_parametres()
    
    if success:
        print("\n✅ CONFIGURATION RÉUSSIE!")
        print("\n📋 RÉSUMÉ:")
        print("1. ✅ Champ numero_patron ajouté au modèle")
        print("2. ✅ Migration appliquée")
        print("3. ✅ Paramètres mis à jour")
        print("4. ✅ Interface patron modifiée")
        print("5. ✅ Messages WhatsApp adaptés")
        print("\n🔧 FONCTIONNALITÉS:")
        print("- Le patron peut configurer son numéro dans les paramètres")
        print("- Tous les messages WhatsApp utilisent ce numéro")
        print("- Fallback vers le numéro par défaut si non configuré")
    else:
        print("\n❌ PROBLÈME DÉTECTÉ!")
        print("Vérifiez les logs pour plus de détails")

if __name__ == '__main__':
    main()
