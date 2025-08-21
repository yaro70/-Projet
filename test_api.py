#!/usr/bin/env python3
"""
Script de test pour vérifier l'API après déploiement
"""
import requests
import json

def test_api():
    # URL de base (à modifier selon votre domaine Render)
    base_url = "https://votre-service.onrender.com"  # Remplacez par votre URL
    
    print("🧪 Test de l'API Pâtisserie")
    print("=" * 50)
    
    # Test 1: Page d'accueil
    print("1. Test page d'accueil...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print("   ✅ Normal - Pas de page d'accueil Django")
        else:
            print(f"   Contenu: {response.text[:100]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: API Gâteaux
    print("\n2. Test API Gâteaux...")
    try:
        response = requests.get(f"{base_url}/api/gateaux/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {len(data)} gâteaux trouvés")
            for gateau in data[:3]:  # Afficher les 3 premiers
                print(f"   - {gateau.get('nom', 'N/A')}: {gateau.get('prix', 'N/A')} FCFA")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: API Paramètres
    print("\n3. Test API Paramètres...")
    try:
        response = requests.get(f"{base_url}/api/parametres/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Paramètres trouvés")
            for param in data:
                print(f"   - Prix livraison: {param.get('prix_livraison', 'N/A')} FCFA")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 4: Admin Django
    print("\n4. Test Admin Django...")
    try:
        response = requests.get(f"{base_url}/admin/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Admin Django accessible")
        elif response.status_code == 302:
            print("   ✅ Admin Django - Redirection vers login (normal)")
        else:
            print(f"   ⚠️ Status inattendu: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n🎉 Test terminé!")
    print("\n📋 Identifiants de test:")
    print("   Admin: admin/admin123")
    print("   Patron: patron/patron123")
    print("   Collaborateur: collaborateur/collaborateur123")

if __name__ == "__main__":
    test_api()
