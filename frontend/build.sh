#!/bin/bash

# Script de build alternatif pour Render
# Ce script force l'utilisation de la bonne commande de build

echo "🚀 Starting build process..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Make sure you're in the frontend directory."
    exit 1
fi

# Installer les dépendances
echo "📦 Installing dependencies..."
npm ci

# Vérifier que le script build existe
if ! npm run | grep -q "build"; then
    echo "❌ Error: build script not found in package.json"
    npm run
    exit 1
fi

# Exécuter le build
echo "🔨 Running build..."
npm run build

echo "✅ Build completed successfully!"
