#!/usr/bin/env python3
import os
import django
import subprocess

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

def create_migration_fix():
    """Créer et appliquer la migration pour corriger les champs DecimalField"""
    
    print("🔧 Création et application de la migration de correction:")
    print("=" * 50)
    
    try:
        # Créer la migration
        print("📝 Création de la migration...")
        result = subprocess.run(['python', 'manage.py', 'makemigrations', 'boutique'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Migration créée avec succès")
            print(result.stdout)
        else:
            print("   ❌ Erreur lors de la création de la migration:")
            print(result.stderr)
            return
        
        # Appliquer la migration
        print("\n📝 Application de la migration...")
        result = subprocess.run(['python', 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Migration appliquée avec succès")
            print(result.stdout)
        else:
            print("   ❌ Erreur lors de l'application de la migration:")
            print(result.stderr)
            return
            
        print("\n🎉 Migration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    create_migration_fix() 