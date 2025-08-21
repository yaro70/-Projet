#!/usr/bin/env python3
"""
Script pour vider le cache des gâteaux
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patisserie_project.settings')
django.setup()

from django.core.cache import cache

def clear_gateaux_cache():
    """Vider le cache des gâteaux"""
    
    print("🗑️ Vidage du cache des gâteaux:")
    print("=" * 40)
    
    # Vider le cache des gâteaux
    cache.delete('public_gateaux')
    print("✅ Cache des gâteaux vidé")
    
    # Vider le cache de la galerie
    cache.delete('galerie_photos')
    print("✅ Cache de la galerie vidé")
    
    print("\n🎉 Cache vidé avec succès!")
    print("📋 Les images devraient maintenant s'afficher correctement")

if __name__ == "__main__":
    clear_gateaux_cache() 