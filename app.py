#!/usr/bin/env python
"""
Fichier app.py pour Render - Redirige vers l'application Django
"""

import os
import sys

# Ajouter le répertoire du projet au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')

# Importer l'application Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
