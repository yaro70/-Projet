#!/usr/bin/env python
"""
WSGI config for patisserie project.
"""

import os
import sys

# Ajouter le répertoire du projet au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings_render')

# Importer l'application Django
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
application = app  # Pour compatibilité
