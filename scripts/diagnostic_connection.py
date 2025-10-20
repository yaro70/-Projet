#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion frontend-backend
"""

import requests
import time
import json

def test_backend_direct():
    """Test direct du backend"""
    print("🔧 Test Backend Direct...")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/login/',
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000'
            },
            json={'username': 'admin', 'password': 'admin123'}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Token: {data['token'][:20]}...")
            print(f"✅ User: {data['username']}")
            return True
        else:
            print(f"❌ Erreur: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_frontend_access():
    """Test d'accès au frontend"""
    print("\n🎨 Test Frontend...")
    
    try:
        response = requests.get("http://localhost:3000")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Frontend accessible")
            return True
        else:
            print(f"❌ Frontend inaccessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend non accessible: {e}")
        return False

def test_cors_preflight():
    """Test CORS preflight"""
    print("\n🌐 Test CORS Preflight...")
    
    try:
        response = requests.options(
            'http://localhost:8000/api/login/',
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ CORS Preflight OK")
            return True
        else:
            print(f"❌ CORS Preflight échoué")
            return False
            
    except Exception as e:
        print(f"❌ Exception CORS: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 DIAGNOSTIC CONNEXION FRONTEND-BACKEND")
    print("=" * 50)
    
    # Attendre que les serveurs démarrent
    print("⏳ Attente du démarrage des serveurs...")
    time.sleep(5)
    
    # Tests
    backend_ok = test_backend_direct()
    frontend_ok = test_frontend_access()
    cors_ok = test_cors_preflight()
    
    print("\n🎯 RÉSULTAT DU DIAGNOSTIC:")
    print("=" * 30)
    print(f"Backend Django: {'✅ OK' if backend_ok else '❌ ERREUR'}")
    print(f"Frontend React: {'✅ OK' if frontend_ok else '❌ ERREUR'}")
    print(f"CORS: {'✅ OK' if cors_ok else '❌ ERREUR'}")
    
    if backend_ok and frontend_ok and cors_ok:
        print("\n🎉 TOUT FONCTIONNE CORRECTEMENT!")
        print("Le problème pourrait être:")
        print("- Cache du navigateur")
        print("- Variables d'environnement")
        print("- Configuration réseau")
    else:
        print("\n⚠️ PROBLÈME DÉTECTÉ!")
        print("Vérifiez les serveurs et la configuration.")

if __name__ == '__main__':
    main()
