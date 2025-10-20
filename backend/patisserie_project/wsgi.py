"""
WSGI config for patisserie_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Définir le module de settings par défaut
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')

application = get_wsgi_application()
