#!/usr/bin/env python3
import sys
import os

print("🔍 Test de l'environnement Python:")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

# Essayer d'importer Django
try:
    import django
    print(f"✅ Django version: {django.get_version()}")
except ImportError as e:
    print(f"❌ Django non trouvé: {e}")

# Essayer d'importer d'autres modules
try:
    import requests
    print("✅ Requests disponible")
except ImportError:
    print("❌ Requests non disponible")

try:
    import rest_framework
    print("✅ Django REST Framework disponible")
except ImportError:
    print("❌ Django REST Framework non disponible") 