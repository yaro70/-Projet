#!/usr/bin/env python3
"""
Test de création d'articles d'événements
"""

import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from django.contrib.auth import authenticate
from boutique.models import User, ArticleEvenement
from rest_framework.authtoken.models import Token
import requests
import json
from datetime import datetime, timedelta
from django.utils import timezone

def test_articles():
    """Test de création d'articles d'événements"""
    
    print("📰 Test de création d'articles:")
    print("=" * 50)
    
    # 1. Connexion d'un patron
    print("\n1️⃣ Connexion patron:")
    patron_username = "deliceDek@ty"
    patron_password = "delicedek@ty123"
    
    try:
        # Authentification Django
        patron = authenticate(username=patron_username, password=patron_password)
        if not patron:
            print("❌ Échec de l'authentification Django")
            return
        
        if not patron.is_patron:
            print("❌ L'utilisateur n'est pas un patron")
            return
        
        print(f"✅ Connexion réussie")
        print(f"👤 Utilisateur: {patron.username}")
        print(f"👑 Rôle: Patron")
        
        # Obtenir le token
        token, _ = Token.objects.get_or_create(user=patron)
        print(f"🔑 Token: {token.key[:20]}...")
        
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return
    
    # 2. Vérifier les articles existants
    print("\n2️⃣ Vérification des articles existants:")
    total_articles = ArticleEvenement.objects.count()
    print(f"📰 Total articles: {total_articles}")
    
    if total_articles > 0:
        print("\n📋 Articles existants:")
        for article in ArticleEvenement.objects.all()[:3]:  # Afficher les 3 premiers
            print(f"  📰 {article.titre} (ID: {article.id})")
            print(f"    📅 Publié le: {article.date_publication.strftime('%d/%m/%Y')}")
    
    # 3. Test de création d'article via API
    print("\n3️⃣ Test de création d'article via API:")
    
    article_data = {
        "titre": "Nouveau Gâteau Spécial",
        "description": "Découvrez notre nouveau gâteau spécial pour les occasions importantes. Un délicieux gâteau au chocolat avec des décorations personnalisées. Parfait pour les anniversaires, mariages et autres célébrations. Commandez dès maintenant pour une expérience gustative exceptionnelle!"
    }
    
    try:
        headers = {
            'Authorization': f'Token {token.key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'http://localhost:8000/api/create-article/',
            json=article_data,
            headers=headers
        )
        
        print(f"📤 Données envoyées: {json.dumps(article_data, indent=2)}")
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Article créé avec succès!")
            print(f"📰 ID: {data['article']['id']}")
            print(f"📰 Titre: {data['article']['titre']}")
            print(f"📰 Description: {data['article']['description'][:100]}...")
            print(f"📅 Date: {data['article']['date_publication']}")
            
            # Vérifier en base de données
            try:
                new_article = ArticleEvenement.objects.get(id=data['article']['id'])
                print(f"✅ Vérification en base: {new_article.titre}")
            except ArticleEvenement.DoesNotExist:
                print("❌ Article non trouvé en base de données")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
    
    # 4. Test avec un utilisateur non-patron
    print("\n4️⃣ Test avec un utilisateur non-patron:")
    
    try:
        # Utiliser le collaborateur pour le test
        collaborateur = authenticate(username="marie_dupont", password="marie123")
        if collaborateur:
            collab_token, _ = Token.objects.get_or_create(user=collaborateur)
            
            headers = {
                'Authorization': f'Token {collab_token.key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                'http://localhost:8000/api/create-article/',
                json=article_data,
                headers=headers
            )
            
            print(f"📥 Statut: {response.status_code}")
            
            if response.status_code == 403:
                print("✅ Accès refusé correctement (seuls les patrons peuvent créer des articles)")
            else:
                print(f"❌ Comportement inattendu: {response.status_code}")
                print(f"📄 Réponse: {response.text}")
                
    except Exception as e:
        print(f"❌ Erreur lors du test collaborateur: {e}")
    
    # 5. Test de récupération des articles
    print("\n5️⃣ Test de récupération des articles:")
    
    try:
        response = requests.get('http://localhost:8000/api/evenements/')
        
        print(f"📥 Statut: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Articles récupérés avec succès!")
            print(f"📰 Nombre d'articles: {len(data)}")
            
            if data:
                print("\n📋 Détails des articles:")
                for article in data[:3]:  # Afficher les 3 premiers
                    print(f"  📰 {article['titre']} (ID: {article['id']})")
                    print(f"    📝 Description: {article['description'][:50]}...")
                    print(f"    📅 Date: {article['date_publication']}")
                    if article['image']:
                        print(f"    🖼️ Image: {article['image']}")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Instructions pour tester dans l'application web:")
    print("1. Aller sur http://localhost:3000/dashboard-patron")
    print("2. Se connecter avec deliceDek@ty / delicedek@ty123")
    print("3. Cliquer sur '📰 Articles' dans la sidebar")
    print("4. Cliquer sur 'Ajouter un article'")
    print("5. Remplir le formulaire et créer l'article")

if __name__ == "__main__":
    test_articles() 