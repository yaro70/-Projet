#!/usr/bin/env python3
"""
Script pour créer des données de test pour les événements et la galerie
"""

import os
import sys
import django
from datetime import datetime, date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import *

def create_test_events():
    """Crée des événements de test"""
    print("📰 Création des événements de test...")
    
    # Supprimer les anciens événements
    ArticleEvenement.objects.all().delete()
    
    events_data = [
        {
            'titre': 'Atelier Pâtisserie pour Enfants',
            'contenu': 'Découvrez l\'art de la pâtisserie avec nos ateliers spécialement conçus pour les enfants. Apprenez à créer de délicieux cupcakes et cookies.',
            'date_evenement': datetime(2024, 12, 25, 14, 0),
            'actif': True
        },
        {
            'titre': 'Formation Gâteaux de Mariage',
            'contenu': 'Formation intensive pour apprendre les techniques de création de gâteaux de mariage élégants et sophistiqués.',
            'date_evenement': datetime(2024, 12, 30, 9, 0),
            'actif': True
        },
        {
            'titre': 'Dégustation de Nouveaux Gâteaux',
            'contenu': 'Venez découvrir nos nouvelles créations et donner votre avis sur nos prochains gâteaux.',
            'date_evenement': datetime(2025, 1, 15, 16, 0),
            'actif': True
        }
    ]
    
    for event_data in events_data:
        ArticleEvenement.objects.create(**event_data)
    
    print(f"✅ {len(events_data)} événements créés")

def create_test_gallery():
    """Crée des photos de galerie de test"""
    print("📸 Création des photos de galerie de test...")
    
    # Supprimer les anciennes photos
    GaleriePhoto.objects.all().delete()
    
    gallery_data = [
        {
            'titre': 'Gâteau d\'Anniversaire Multicolore',
            'description': 'Magnifique gâteau d\'anniversaire avec des couleurs vives et des décorations festives',
            'categorie': 'gateaux',
            'date_realisation': date(2024, 10, 15),
            'ordre_affichage': 10,
            'visible': True
        },
        {
            'titre': 'Atelier Pâtisserie Enfants',
            'description': 'Photos de notre dernier atelier pâtisserie pour enfants',
            'categorie': 'ateliers',
            'date_realisation': date(2024, 11, 20),
            'ordre_affichage': 9,
            'visible': True
        },
        {
            'titre': 'Gâteau de Mariage Élégant',
            'description': 'Gâteau de mariage sophistiqué avec décorations florales',
            'categorie': 'gateaux',
            'date_realisation': date(2024, 9, 10),
            'ordre_affichage': 8,
            'visible': True
        },
        {
            'titre': 'Événement Dégustation',
            'description': 'Photos de notre dernier événement de dégustation',
            'categorie': 'evenements',
            'date_realisation': date(2024, 12, 5),
            'ordre_affichage': 7,
            'visible': True
        }
    ]
    
    for photo_data in gallery_data:
        GaleriePhoto.objects.create(**photo_data)
    
    print(f"✅ {len(gallery_data)} photos de galerie créées")

def main():
    """Fonction principale"""
    print("🔧 Création des données de test")
    print("=" * 40)
    
    try:
        create_test_events()
        create_test_gallery()
        
        print("\n🎉 Données de test créées avec succès!")
        
        # Afficher les statistiques
        print(f"\n📊 Statistiques:")
        print(f"   - Événements: {ArticleEvenement.objects.count()}")
        print(f"   - Photos galerie: {GaleriePhoto.objects.count()}")
        print(f"   - Gâteaux: {Gateau.objects.count()}")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

