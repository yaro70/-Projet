#!/usr/bin/env python3
import os
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import Gateau

def add_images_to_gateaux():
    """Ajouter des images par défaut aux gâteaux"""
    
    print("🖼️  Ajout d'images par défaut aux gâteaux:")
    print("=" * 50)
    
    # Créer le dossier media s'il n'existe pas
    media_dir = os.path.join(os.getcwd(), 'media')
    gateaux_dir = os.path.join(media_dir, 'gateaux')
    
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
        print("   📁 Dossier media créé")
    
    if not os.path.exists(gateaux_dir):
        os.makedirs(gateaux_dir)
        print("   📁 Dossier gateaux créé")
    
    # Vérifier les gâteaux existants
    gateaux = Gateau.objects.all()
    print(f"   📊 Nombre de gâteaux: {gateaux.count()}")
    
    # Images par défaut selon le type
    default_images = {
        'anniversaire': 'gateaux/anniversaire.jpg',
        'mariage': 'gateaux/mariage.jpg',
        'autre': 'gateaux/autre.jpg'
    }
    
    for gateau in gateaux:
        print(f"   🎂 {gateau.nom}:")
        
        if gateau.image:
            print(f"      ✅ Déjà une image: {gateau.image}")
        else:
            # Assigner une image par défaut selon le type
            default_image = default_images.get(gateau.type, 'gateaux/autre.jpg')
            gateau.image = default_image
            gateau.save()
            print(f"      ➕ Image ajoutée: {default_image}")
    
    print("\n🎉 Images ajoutées avec succès!")
    print("\n📋 Prochaines étapes:")
    print("   1. Ajouter des vraies images dans le dossier media/gateaux/")
    print("   2. Redémarrer le serveur Django")
    print("   3. Tester l'affichage dans l'application")

if __name__ == '__main__':
    add_images_to_gateaux() 