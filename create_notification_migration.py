#!/usr/bin/env python3
"""
Création et application de la migration pour les notifications
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from django.core.management import call_command
import subprocess

def create_notification_migration():
    """Créer et appliquer la migration pour les notifications"""
    
    print("🔔 Création et application de la migration des notifications:")
    print("=" * 60)
    
    try:
        # 1. Créer la migration
        print("\n1️⃣ Création de la migration...")
        call_command('makemigrations', 'boutique')
        print("✅ Migration créée avec succès")
        
        # 2. Appliquer la migration
        print("\n2️⃣ Application de la migration...")
        call_command('migrate')
        print("✅ Migration appliquée avec succès")
        
        # 3. Vérifier les modèles
        print("\n3️⃣ Vérification des modèles...")
        from boutique.models import Notification
        
        # Vérifier que le modèle existe
        print(f"✅ Modèle Notification disponible")
        print(f"📊 Champs: {[field.name for field in Notification._meta.fields]}")
        
        # 4. Test de création d'une notification
        print("\n4️⃣ Test de création d'une notification...")
        from boutique.models import User
        
        # Trouver un utilisateur pour le test
        user = User.objects.first()
        if user:
            notification = Notification.objects.create(
                recipient=user,
                notification_type='system_message',
                title='Test de notification',
                message='Ceci est un test du système de notifications',
                data={'test': True}
            )
            print(f"✅ Notification créée: #{notification.id}")
            print(f"📰 Titre: {notification.title}")
            print(f"👤 Destinataire: {notification.recipient.username}")
            print(f"📊 Type: {notification.notification_type}")
            
            # Nettoyer le test
            notification.delete()
            print("🧹 Notification de test supprimée")
        else:
            print("❌ Aucun utilisateur trouvé pour le test")
        
        print("\n🎉 Migration des notifications terminée avec succès!")
        print("\n📋 Prochaines étapes:")
        print("1. Installer les dépendances: pip install channels==4.0.0")
        print("2. Tester le système: python test_notifications.py")
        print("3. Démarrer le serveur: python manage.py runserver")
        print("4. Tester les WebSockets dans l'application web")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_notification_migration() 