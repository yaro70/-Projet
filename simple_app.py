#!/usr/bin/env python
"""
Application simple pour Render
"""

import os
import sys

# Ajouter le répertoire du projet au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')

# Importer Django
import django
django.setup()

# Importer l'application WSGI
from django.core.wsgi import get_wsgi_application

# Créer l'application
app = get_wsgi_application()
