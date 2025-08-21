#!/usr/bin/env python
"""
Script de build simple pour Render
"""

import os
import sys
import subprocess

def run_command(command):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 Exécution: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Succès: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e.stderr}")
        return False

def main():
    print("🚀 Démarrage du build simple...")
    
    # Installer les dépendances
    if not run_command("pip install -r requirements.txt"):
        print("❌ Échec de l'installation des dépendances")
        return
    
    # Configurer Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')
    
    # Importer Django
    import django
    django.setup()
    
    # Créer les migrations
    if not run_command("python manage.py makemigrations boutique --noinput"):
        print("⚠️ Erreur lors de la création des migrations")
    
    # Appliquer les migrations
    if not run_command("python manage.py migrate --noinput"):
        print("❌ Échec des migrations")
        return
    
    # Collecter les fichiers statiques
    if not run_command("python manage.py collectstatic --noinput"):
        print("⚠️ Erreur lors de la collecte des fichiers statiques")
    
    # Créer les données de test
    print("📝 Création des données de test...")
    try:
        from django.contrib.auth import get_user_model
        from boutique.models import *
        from decimal import Decimal
        
        User = get_user_model()
        
        # Créer superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superuser créé: admin/admin123")
        
        # Créer gâteaux
        if Gateau.objects.count() == 0:
            gateaux_data = [
                {'nom': 'Gâteau d\'Anniversaire Chocolat', 'description': 'Délicieux gâteau au chocolat', 'prix': Decimal('15000.00')},
                {'nom': 'Gâteau de Mariage Vanille', 'description': 'Magnifique gâteau de mariage', 'prix': Decimal('25000.00')},
                {'nom': 'Cupcakes Assortis', 'description': 'Assortiment de cupcakes', 'prix': Decimal('8000.00')},
            ]
            
            for data in gateaux_data:
                Gateau.objects.create(**data)
            print(f"✅ {len(gateaux_data)} gâteaux créés")
        
        # Créer paramètres
        if ParametresLivraison.objects.count() == 0:
            ParametresLivraison.objects.create(prix_livraison=Decimal('2000.00'))
            print("✅ Paramètres de livraison créés")
        
        # Créer utilisateurs
        if User.objects.filter(is_patron=True).count() == 0:
            User.objects.create_user('patron', 'patron@example.com', 'patron123', is_patron=True)
            print("✅ Patron créé: patron/patron123")
        
        if User.objects.filter(is_collaborateur=True).count() == 0:
            User.objects.create_user('collaborateur', 'collaborateur@example.com', 'collaborateur123', is_collaborateur=True)
            print("✅ Collaborateur créé: collaborateur/collaborateur123")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la création des données: {e}")
    
    print("🎉 Build terminé avec succès!")

if __name__ == '__main__':
    main()
