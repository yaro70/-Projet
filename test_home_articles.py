#!/usr/bin/env python3
"""
Test de l'affichage des articles sur la page d'accueil
"""

import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import ArticleEvenement
import requests
import json

def test_home_articles():
    """Test de l'affichage des articles sur la page d'accueil"""
    
    print("🏠 Test de l'affichage des articles sur la page d'accueil:")
    print("=" * 60)
    
    # 1. Vérifier les articles existants
    print("\n1️⃣ Vérification des articles existants:")
    total_articles = ArticleEvenement.objects.count()
    print(f"📰 Total articles: {total_articles}")
    
    if total_articles > 0:
        print("\n📋 Articles disponibles:")
        for article in ArticleEvenement.objects.all():
            print(f"  📰 {article.titre} (ID: {article.id})")
            print(f"    📝 Description: {article.description[:50]}...")
            print(f"    📅 Publié le: {article.date_publication.strftime('%d/%m/%Y')}")
            print(f"    🖼️ Image: {'Oui' if article.image else 'Non'}")
    else:
        print("ℹ️ Aucun article disponible")
        return
    
    # 2. Test de l'API des articles (accessible publiquement)
    print("\n2️⃣ Test de l'API des articles (page d'accueil):")
    
    try:
        response = requests.get('http://localhost:8000/api/evenements/')
        
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Articles récupérés avec succès!")
            print(f"📰 Nombre d'articles: {len(data)}")
            
            if data:
                print("\n📋 Détails des articles (API):")
                for article in data:
                    print(f"  📰 {article['titre']} (ID: {article['id']})")
                    print(f"    📝 Description: {article['description'][:50]}...")
                    print(f"    📅 Date: {article['date_publication']}")
                    if article['image']:
                        print(f"    🖼️ Image: {article['image']}")
                    else:
                        print(f"    🖼️ Image: Aucune")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération: {e}")
    
    # 3. Test de création d'un article supplémentaire
    print("\n3️⃣ Test de création d'un article supplémentaire:")
    
    try:
        # Créer un nouvel article pour tester
        nouvel_article = ArticleEvenement.objects.create(
            titre="Promotion Spéciale - Gâteaux d'Anniversaire",
            description="Profitez de notre promotion spéciale sur tous nos gâteaux d'anniversaire ! Réduction de 15% sur tous les gâteaux commandés cette semaine. Parfait pour célébrer vos moments spéciaux avec style et saveur. Offre limitée, commandez vite !"
        )
        
        print(f"✅ Nouvel article créé: #{nouvel_article.id}")
        print(f"📰 Titre: {nouvel_article.titre}")
        print(f"📝 Description: {nouvel_article.description[:50]}...")
        
        # Vérifier le total après création
        total_apres = ArticleEvenement.objects.count()
        print(f"📊 Total articles après création: {total_apres}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
    
    # 4. Test de récupération après création
    print("\n4️⃣ Test de récupération après création:")
    
    try:
        response = requests.get('http://localhost:8000/api/evenements/')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {len(data)} articles maintenant disponibles")
            
            # Vérifier que le nouvel article est présent
            nouvel_article_api = next((a for a in data if a['titre'] == "Promotion Spéciale - Gâteaux d'Anniversaire"), None)
            if nouvel_article_api:
                print("✅ Nouvel article trouvé dans l'API")
            else:
                print("❌ Nouvel article non trouvé dans l'API")
                
        else:
            print(f"❌ Erreur API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("1. Aller sur http://localhost:3000")
    print("2. Voir la section '📰 Actualités & Événements'")
    print("3. Vérifier que les articles s'affichent correctement")
    print("4. Tester avec différents navigateurs/devices")

if __name__ == "__main__":
    test_home_articles() 