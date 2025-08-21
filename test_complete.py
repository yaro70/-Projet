#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User, Gateau, ParametresLivraison
from django.contrib.auth import authenticate

def test_complete():
    """Test complet de l'application"""
    
    print("🧪 Test complet de l'application:")
    print("=" * 50)
    
    # 1. Test des utilisateurs
    print("\n1️⃣ Test des utilisateurs:")
    users = User.objects.all()
    for user in users:
        print(f"   - {user.username}: Patron={user.is_patron}, Collaborateur={user.is_collaborateur}")
        
        # Test d'authentification
        password = f"{user.username.lower()}123"
        auth_user = authenticate(username=user.username, password=password)
        if auth_user:
            print(f"     ✅ Authentification réussie avec: {password}")
        else:
            print(f"     ❌ Authentification échouée avec: {password}")
    
    # 2. Test des gâteaux
    print("\n2️⃣ Test des gâteaux:")
    gateaux = Gateau.objects.all()
    if gateaux.count() == 0:
        print("   ⚠️  Aucun gâteau trouvé - exécutez 'python add_gateaux.py'")
    else:
        for gateau in gateaux:
            print(f"   - {gateau.nom}: {gateau.prix} FCFA ({gateau.type})")
    
    # 3. Test des paramètres
    print("\n3️⃣ Test des paramètres:")
    parametres = ParametresLivraison.objects.all()
    for param in parametres:
        print(f"   - Prix livraison: {param.prix_livraison} FCFA")
    
    # 4. Test de l'API
    print("\n4️⃣ Test de l'API:")
    try:
        # Test API publique gâteaux
        response = requests.get('http://localhost:8000/api/public/gateaux/')
        if response.status_code == 200:
            gateaux_api = response.json()
            print(f"   ✅ API publique gâteaux: {len(gateaux_api)} gâteaux")
        else:
            print(f"   ❌ API publique gâteaux: {response.status_code}")
        
        # Test API paramètres
        response = requests.get('http://localhost:8000/api/parametres/')
        if response.status_code == 200:
            params_api = response.json()
            print(f"   ✅ API paramètres: {len(params_api)} paramètre(s)")
        else:
            print(f"   ❌ API paramètres: {response.status_code}")
        
        # Test connexion
        response = requests.post('http://localhost:8000/api/login/', 
                               json={'username': 'deliceDek@ty', 'password': 'delicedek@ty123'})
        if response.status_code == 200:
            print("   ✅ API connexion fonctionne")
            token = response.json()['token']
            
            # Test API commandes avec token
            headers = {'Authorization': f'Token {token}'}
            response = requests.get('http://localhost:8000/api/commandes/', headers=headers)
            if response.status_code == 200:
                print("   ✅ API commandes fonctionne")
            else:
                print(f"   ❌ API commandes: {response.status_code}")
        else:
            print("   ❌ API connexion échoue")
            
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Serveur Django non démarré")
    except Exception as e:
        print(f"   ❌ Erreur API: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Résumé:")
    print(f"   - {users.count()} utilisateur(s)")
    print(f"   - {gateaux.count()} gâteau(x)")
    print(f"   - {parametres.count()} paramètre(s)")
    
    if gateaux.count() == 0:
        print("\n⚠️  Actions recommandées:")
        print("   1. Exécuter: python add_gateaux.py")
        print("   2. Redémarrer le serveur: python manage.py runserver 8000")
        print("   3. Tester l'application: http://localhost:3000")

if __name__ == '__main__':
    test_complete() 