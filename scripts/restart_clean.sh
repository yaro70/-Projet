#!/bin/bash
# Script pour nettoyer le cache et redémarrer les serveurs

echo "🧹 NETTOYAGE CACHE ET REDÉMARRAGE"
echo "=================================="

# Arrêter tous les processus
echo "⏹️ Arrêt des serveurs..."
pkill -f "python manage.py runserver"
pkill -f "react-scripts start"
sleep 2

# Nettoyer le cache React
echo "🧹 Nettoyage du cache React..."
cd /home/yaro/Desktop/Projet/patisserie_project/frontend
rm -rf node_modules/.cache
rm -rf build
npm cache clean --force

# Redémarrer le backend
echo "🚀 Redémarrage du backend Django..."
cd /home/yaro/Desktop/Projet/patisserie_project/backend
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!

# Attendre que le backend démarre
echo "⏳ Attente du démarrage du backend..."
sleep 5

# Redémarrer le frontend
echo "🚀 Redémarrage du frontend React..."
cd /home/yaro/Desktop/Projet/patisserie_project/frontend
npm start &
FRONTEND_PID=$!

echo "✅ Serveurs redémarrés!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "🌐 URLs d'accès:"
echo "- Frontend: http://localhost:3000"
echo "- Backend: http://localhost:8000"
echo ""
echo "🔑 Identifiants de test:"
echo "- Admin: admin / admin123"
echo "- Patron: patron / patron123"
echo "- Collaborateur: collaborateur / collaborateur123"
echo ""
echo "💡 Si le problème persiste:"
echo "1. Videz le cache de votre navigateur (Ctrl+Shift+R)"
echo "2. Ouvrez les outils de développement (F12)"
echo "3. Vérifiez l'onglet Network pour voir les requêtes"
echo "4. Essayez en navigation privée"
