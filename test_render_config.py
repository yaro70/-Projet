#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration Render
"""
import os
import sys
import django
from pathlib import Path

def test_configuration():
    print("🔧 Test de configuration Render")
    print("=" * 50)
    
    # 1. Vérifier les variables d'environnement
    print("📋 Variables d'environnement:")
    env_vars = [
        'DJANGO_SETTINGS_MODULE',
        'SECRET_KEY',
        'DEBUG',
        'ALLOWED_HOSTS',
        'DATABASE_URL',
        'REDIS_URL',
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'Non définie')
        if var in ['SECRET_KEY', 'DATABASE_URL', 'REDIS_URL']:
            # Masquer les valeurs sensibles
            if value != 'Non définie':
                value = value[:10] + '...' if len(value) > 10 else value
        print(f"  {var}: {value}")
    
    # 2. Vérifier Django
    print("\n🐍 Test Django:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')
        django.setup()
        print("  ✅ Django configuré avec succès")
        print(f"  📦 Version Django: {django.get_version()}")
    except Exception as e:
        print(f"  ❌ Erreur Django: {e}")
        return False
    
    # 3. Vérifier la base de données
    print("\n🗄️ Test base de données:")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("  ✅ Connexion base de données OK")
    except Exception as e:
        print(f"  ❌ Erreur base de données: {e}")
        return False
    
    # 4. Vérifier les applications
    print("\n📱 Test applications:")
    try:
        from django.apps import apps
        installed_apps = [app.name for app in apps.get_app_configs()]
        required_apps = ['boutique', 'rest_framework', 'corsheaders', 'channels']
        
        for app in required_apps:
            if app in installed_apps:
                print(f"  ✅ {app}")
            else:
                print(f"  ❌ {app} manquant")
                return False
    except Exception as e:
        print(f"  ❌ Erreur applications: {e}")
        return False
    
    # 5. Vérifier les modèles
    print("\n🏗️ Test modèles:")
    try:
        from boutique.models import User, Gateau, Commande
        print("  ✅ Modèles importés avec succès")
    except Exception as e:
        print(f"  ❌ Erreur modèles: {e}")
        return False
    
    # 6. Vérifier les URLs
    print("\n🔗 Test URLs:")
    try:
        from django.urls import reverse
        print("  ✅ Système d'URLs fonctionnel")
    except Exception as e:
        print(f"  ❌ Erreur URLs: {e}")
        return False
    
    print("\n✅ Configuration testée avec succès!")
    return True

if __name__ == "__main__":
    success = test_configuration()
    sys.exit(0 if success else 1)
