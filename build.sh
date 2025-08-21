#!/usr/bin/env bash
# Script de build automatique pour Render (Plan Gratuit)

set -e  # Arrêter le script en cas d'erreur

echo "🚀 Démarrage du build automatique (Plan Gratuit)..."

# Vérifier la version Python
echo "🐍 Version Python:"
python --version

# Mettre à jour pip
echo "📦 Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Installer Pillow (optionnel)
echo "📦 Installation de Pillow (optionnel)..."
pip install Pillow==11.3.0 || echo "⚠️ Pillow non installé, images désactivées"

# Vérifier Django
echo "🔍 Vérification de Django..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Vérifier la configuration
echo "⚙️ Vérification de la configuration..."
python manage.py check --deploy

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate --noinput

# Créer un superuser automatiquement
echo "👤 Création d'un superuser par défaut..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser créé: admin/admin123')
else:
    print('ℹ️ Superuser existe déjà')
"

# Créer les données de test de manière sécurisée
echo "📊 Création des données de test..."
python manage.py shell -c "
try:
    from boutique.models import *
    from decimal import Decimal
    from django.utils import timezone
    
    # Créer des gâteaux de test
    if Gateau.objects.count() == 0:
        gateaux_data = [
            {'nom': 'Gâteau d\'Anniversaire Chocolat', 'description': 'Délicieux gâteau au chocolat pour anniversaire', 'prix': Decimal('15000.00')},
            {'nom': 'Gâteau de Mariage Vanille', 'description': 'Magnifique gâteau de mariage à la vanille', 'prix': Decimal('25000.00')},
            {'nom': 'Cupcakes Assortis', 'description': 'Assortiment de cupcakes colorés', 'prix': Decimal('8000.00')},
            {'nom': 'Gâteau au Citron', 'description': 'Gâteau frais au citron', 'prix': Decimal('12000.00')},
            {'nom': 'Gâteau Red Velvet', 'description': 'Gâteau rouge velours élégant', 'prix': Decimal('18000.00')},
        ]
        
        for data in gateaux_data:
            Gateau.objects.create(**data)
        print(f'✅ {len(gateaux_data)} gâteaux créés')
    else:
        print(f'ℹ️ {Gateau.objects.count()} gâteaux existent déjà')

    # Créer des paramètres de livraison
    if ParametresLivraison.objects.count() == 0:
        ParametresLivraison.objects.create(prix_livraison=Decimal('2000.00'))
        print('✅ Paramètres de livraison créés')
    else:
        print('ℹ️ Paramètres de livraison existent déjà')

    # Créer des utilisateurs de test
    if User.objects.filter(is_patron=True).count() == 0:
        patron = User.objects.create_user(
            username='patron',
            email='patron@example.com',
            password='patron123',
            is_patron=True
        )
        print('✅ Patron créé: patron/patron123')
    else:
        print('ℹ️ Patron existe déjà')

    if User.objects.filter(is_collaborateur=True).count() == 0:
        collaborateur = User.objects.create_user(
            username='collaborateur',
            email='collaborateur@example.com',
            password='collaborateur123',
            is_collaborateur=True
        )
        print('✅ Collaborateur créé: collaborateur/collaborateur123')
    else:
        print('ℹ️ Collaborateur existe déjà')

    print('🎉 Données de test créées avec succès!')
except Exception as e:
    print(f'❌ Erreur lors de la création des données: {e}')
    print('⚠️ Continuation du build...')
"

# Vérifier que l'application peut démarrer
echo "🔧 Test de démarrage de l'application..."
python manage.py check

echo "✅ Build terminé avec succès! (Plan Gratuit)"

