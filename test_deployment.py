#!/usr/bin/env python
"""
Script de test complet pour vérifier le déploiement
"""

import requests
import json
from datetime import datetime

def test_deployment():
    print("🧪 Test complet du déploiement")
    print("=" * 50)
    
    # URLs de test
    backend_url = "https://projet-c2vz.onrender.com"
    frontend_url = "https://patisserie-frontend.onrender.com"
    
    tests = [
        {
            "name": "Frontend React",
            "url": frontend_url,
            "expected_status": 200
        },
        {
            "name": "API Gâteaux Public",
            "url": f"{backend_url}/api/public/gateaux/",
            "expected_status": 200
        },
        {
            "name": "API Paramètres",
            "url": f"{backend_url}/api/parametres/",
            "expected_status": 200
        },
        {
            "name": "Admin Django",
            "url": f"{backend_url}/admin/",
            "expected_status": 302  # Redirection vers login
        },
        {
            "name": "API Root",
            "url": f"{backend_url}/",
            "expected_status": 404  # Normal, pas de page racine
        }
    ]
    
    results = []
    
    for test in tests:
        try:
            print(f"🔍 Test: {test['name']}")
            response = requests.get(test['url'], timeout=10)
            
            if response.status_code == test['expected_status']:
                print(f"✅ {test['name']}: OK ({response.status_code})")
                results.append(True)
            else:
                print(f"❌ {test['name']}: Erreur ({response.status_code} au lieu de {test['expected_status']})")
                results.append(False)
                
            # Afficher des détails pour l'API gâteaux
            if "gateaux" in test['url'] and response.status_code == 200:
                try:
                    data = response.json()
                    gateaux_count = len(data.get('gateaux', []))
                    print(f"   📊 {gateaux_count} gâteaux trouvés")
                    
                    if gateaux_count > 0:
                        premier_gateau = data['gateaux'][0]
                        print(f"   🎂 Premier gâteau: {premier_gateau.get('nom', 'N/A')} - {premier_gateau.get('prix', 'N/A')} FCFA")
                except:
                    print("   ⚠️ Erreur parsing JSON")
                    
        except Exception as e:
            print(f"❌ {test['name']}: Erreur - {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Résultats du test:")
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"✅ Tests réussis: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 Tous les tests sont passés ! Le déploiement est réussi !")
        print("\n🌐 URLs d'accès:")
        print(f"   Frontend: {frontend_url}")
        print(f"   Backend API: {backend_url}/api/")
        print(f"   Admin: {backend_url}/admin/")
        print("\n🔑 Identifiants de test:")
        print("   Admin: admin/admin123")
        print("   Patron: patron/patron123")
        print("   Collaborateur: collaborateur/collaborateur123")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
    
    return success_count == total_count

if __name__ == '__main__':
    test_deployment()
