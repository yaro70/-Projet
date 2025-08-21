#!/usr/bin/env python3
import os
import django
import subprocess

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

def create_whatsapp_migration():
    """Créer et appliquer la migration pour les champs WhatsApp"""
    
    print("📱 Création de la migration WhatsApp:")
    print("=" * 40)
    
    try:
        # Créer la migration
        print("📝 Création de la migration...")
        result = subprocess.run(['python', 'manage.py', 'makemigrations', 'boutique'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Migration créée avec succès")
            if result.stdout:
                print(f"   📄 Sortie: {result.stdout}")
        else:
            print("   ❌ Erreur lors de la création de la migration:")
            print(f"   📄 Erreur: {result.stderr}")
            return
        
        # Appliquer la migration
        print("\n📝 Application de la migration...")
        result = subprocess.run(['python', 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Migration appliquée avec succès")
            if result.stdout:
                print(f"   📄 Sortie: {result.stdout}")
        else:
            print("   ❌ Erreur lors de l'application de la migration:")
            print(f"   📄 Erreur: {result.stderr}")
            return
        
        print("\n🎉 Migration WhatsApp terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    create_whatsapp_migration() 