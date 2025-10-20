#!/bin/bash

# Script de déploiement pour Render
# Ce script prépare le projet pour le déploiement

echo "🚀 Préparation du déploiement sur Render..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "render.yaml" ]; then
    echo "❌ Erreur: render.yaml non trouvé. Exécutez ce script depuis la racine du projet."
    exit 1
fi

# Nettoyer les builds précédents
echo "🧹 Nettoyage des builds précédents..."
rm -rf frontend/build
rm -rf backend/staticfiles
rm -rf backend/__pycache__
rm -rf backend/boutique/__pycache__

# Vérifier les dépendances frontend
echo "📦 Vérification des dépendances frontend..."
cd frontend
if [ ! -f "package-lock.json" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Test du build frontend
echo "🔨 Test du build frontend..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du build frontend"
    exit 1
fi

cd ..

# Vérifier les dépendances backend
echo "🐍 Vérification des dépendances backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "⚠️  Environnement virtuel Python non trouvé"
fi

# Test des migrations
echo "🗄️  Test des migrations..."
python manage.py check --deploy
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de la vérification Django"
    exit 1
fi

cd ..

echo "✅ Projet prêt pour le déploiement sur Render!"
echo ""
echo "📋 Étapes suivantes:"
echo "1. Commitez vos changements: git add . && git commit -m 'Fix deployment configuration'"
echo "2. Poussez vers GitHub: git push origin main"
echo "3. Le déploiement se lancera automatiquement sur Render"
echo ""
echo "🔗 URLs attendues:"
echo "- Backend: https://patisserie-backend.onrender.com"
echo "- Frontend: https://patisserie-frontend.onrender.com"
