#!/usr/bin/env python3
"""
Script de configuration automatique pour le projet Pâtisserie
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 Exécution: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
        print(f"✅ Succès: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e.stderr}")
        return False

def setup_backend():
    """Configure le backend Django"""
    print("🚀 Configuration du backend Django...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Dossier backend non trouvé")
        return False
    
    # Créer un environnement virtuel
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("📦 Création de l'environnement virtuel...")
        if not run_command("python3 -m venv venv", cwd=backend_dir):
            return False
    
    # Activer l'environnement virtuel et installer les dépendances
    if os.name == 'nt':  # Windows
        pip_cmd = str(venv_dir / "Scripts" / "pip")
        python_cmd = str(venv_dir / "Scripts" / "python")
    else:  # Linux/Mac
        pip_cmd = str(venv_dir / "bin" / "pip")
        python_cmd = str(venv_dir / "bin" / "python")
    
    # Vérifier que les commandes existent
    if not os.path.exists(pip_cmd):
        print(f"❌ Pip non trouvé : {pip_cmd}")
        return False
    if not os.path.exists(python_cmd):
        print(f"❌ Python non trouvé : {python_cmd}")
        return False
    
    print("📦 Installation des dépendances...")
    if not run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir):
        return False
    
    # Appliquer les migrations
    print("🗄️ Application des migrations...")
    if not run_command(f"{python_cmd} manage.py migrate", cwd=backend_dir):
        return False
    
    # Créer les utilisateurs de test
    print("👤 Création des utilisateurs de test...")
    try:
        # Script Python pour créer les utilisateurs
        create_users_script = """
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Créer admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Admin créé: admin/admin123')

# Créer patron
if not User.objects.filter(username='patron').exists():
    User.objects.create_user('patron', 'patron@example.com', 'patron123', is_patron=True, is_staff=True)
    print('✅ Patron créé: patron/patron123')

# Créer collaborateur
if not User.objects.filter(username='collaborateur').exists():
    User.objects.create_user('collaborateur', 'collaborateur@example.com', 'collaborateur123', is_collaborateur=True)
    print('✅ Collaborateur créé: collaborateur/collaborateur123')
"""
        
        # Écrire le script temporaire
        with open(backend_dir / "create_users.py", "w") as f:
            f.write(create_users_script)
        
        # Exécuter le script
        run_command(f"{python_cmd} create_users.py", cwd=backend_dir)
        
        # Supprimer le script temporaire
        os.remove(backend_dir / "create_users.py")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la création des utilisateurs: {e}")
    
    # Collecter les fichiers statiques
    print("📁 Collecte des fichiers statiques...")
    run_command(f"{python_cmd} manage.py collectstatic --noinput", cwd=backend_dir)
    
    print("✅ Backend configuré avec succès!")
    return True

def setup_frontend():
    """Configure le frontend React"""
    print("🎨 Configuration du frontend React...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Dossier frontend non trouvé")
        return False
    
    # Installer les dépendances
    print("📦 Installation des dépendances npm...")
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    print("✅ Frontend configuré avec succès!")
    return True

def create_env_files():
    """Crée les fichiers d'environnement"""
    print("📝 Création des fichiers d'environnement...")
    
    # Backend .env
    backend_env = """# Configuration Backend Django
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Channels
CHANNEL_LAYERS_BACKEND=channels.layers.InMemoryChannelLayer

# Cache
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
"""
    
    with open("backend/.env", "w") as f:
        f.write(backend_env)
    
    # Frontend .env
    frontend_env = """# Configuration Frontend React
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
"""
    
    with open("frontend/.env", "w") as f:
        f.write(frontend_env)
    
    print("✅ Fichiers d'environnement créés!")

def main():
    """Fonction principale"""
    print("🎂 Configuration du Projet Pâtisserie")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Veuillez exécuter ce script depuis la racine du projet")
        return False
    
    # Créer les fichiers d'environnement
    create_env_files()
    
    # Configurer le backend
    if not setup_backend():
        print("❌ Échec de la configuration du backend")
        return False
    
    # Configurer le frontend
    if not setup_frontend():
        print("❌ Échec de la configuration du frontend")
        return False
    
    print("\n🎉 Configuration terminée avec succès!")
    print("\n📋 Prochaines étapes:")
    print("1. Backend: cd backend && source venv/bin/activate && python manage.py runserver")
    print("2. Frontend: cd frontend && npm start")
    print("\n🌐 URLs:")
    print("- Frontend: http://localhost:3000")
    print("- Backend: http://localhost:8000")
    print("- Admin: http://localhost:8000/admin/")
    print("\n🔑 Identifiants:")
    print("- Username: admin")
    print("- Password: admin123")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
