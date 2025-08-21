#!/usr/bin/env python3
import os
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from boutique.models import User, Gateau, Commande, ParametresLivraison
from django.contrib.auth import authenticate

def test_complete_app():
    """Tester l'application complète"""
    
    print("🧪 Test complet de l'application:")
    print("=" * 50)
    
    # 1. Test des utilisateurs
    print("\n1️⃣ Test des utilisateurs:")
    users = User.objects.all()
    for user in users:
        print(f"   - {user.username}: Patron={user.is_patron}, Collaborateur={user.is_collaborateur}")
    
    # 2. Test des gâteaux
    print("\n2️⃣ Test des gâteaux:")
    gateaux = Gateau.objects.all()
    for gateau in gateaux:
        print(f"   - {gateau.nom}: {gateau.prix} FCFA ({gateau.type})")
    
    # 3. Test des paramètres
    print("\n3️⃣ Test des paramètres:")
    parametres = ParametresLivraison.objects.all()
    for param in parametres:
        print(f"   - Prix livraison: {param.prix_livraison} FCFA")
    
    # 4. Test des commandes
    print("\n4️⃣ Test des commandes:")
    commandes = Commande.objects.all()
    for cmd in commandes:
        print(f"   - Commande #{cmd.id}: {cmd.client_nom} - {cmd.status}")
    
    # 5. Test de l'API
    print("\n5️⃣ Test de l'API:")
    try:
        # Test connexion
        response = requests.post('http://localhost:8000/api/login/', 
                               json={'username': 'test', 'password': 'test123'})
        if response.status_code == 200:
            print("   ✅ API de connexion fonctionne")
            token = response.json()['token']
            
            # Test récupération gâteaux
            headers = {'Authorization': f'Token {token}'}
            g_response = requests.get('http://localhost:8000/api/gateaux/', headers=headers)
            if g_response.status_code == 200:
                print(f"   ✅ API gâteaux fonctionne ({len(g_response.json())} gâteaux)")
            
            # Test récupération commandes
            c_response = requests.get('http://localhost:8000/api/commandes/', headers=headers)
            if c_response.status_code == 200:
                print(f"   ✅ API commandes fonctionne ({len(c_response.json())} commandes)")
                
        else:
            print("   ❌ API de connexion échoue")
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Serveur Django non démarré")
    except Exception as e:
        print(f"   ❌ Erreur API: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Résumé:")
    print(f"   - {users.count()} utilisateurs")
    print(f"   - {gateaux.count()} gâteaux")
    print(f"   - {parametres.count()} paramètre(s)")
    print(f"   - {commandes.count()} commande(s)")

if __name__ == '__main__':
    test_complete_app() 