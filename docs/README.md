# 🎂 Patisserie Management System

## 📋 Vue d'ensemble

Système de gestion complet pour une pâtisserie avec :
- **Backend** : Django REST API + WebSockets
- **Frontend** : React + Material-UI
- **Base de données** : SQLite/PostgreSQL
- **Déploiement** : Render (automatique)

## 🏗️ Architecture

```
patisserie_project/
├── backend/                 # API Django
│   ├── boutique/           # Application principale
│   ├── patisserie_project/ # Configuration Django
│   └── manage.py
├── frontend/               # Interface React
│   ├── src/
│   │   ├── components/     # Composants React
│   │   ├── config.js      # Configuration API
│   │   └── App.js
│   └── package.json
├── docs/                   # Documentation
├── scripts/               # Scripts utilitaires
├── deploy/                # Configuration déploiement
└── README.md
```

## 🚀 Déploiement Rapide

### Option 1 : Déploiement Automatique (Recommandé)
1. Connectez votre repo GitHub à Render
2. Utilisez le Blueprint `deploy/render.yaml`
3. C'est tout ! 🎉

### Option 2 : Déploiement Manuel
```bash
# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm start
```

## 🔑 Accès par Défaut

| Rôle | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `admin123` |
| **Patron** | `patron` | `patron123` |
| **Collaborateur** | `collaborateur` | `collaborateur123` |

## 📚 Documentation Complète

- [Guide d'installation](docs/INSTALLATION.md)
- [Configuration](docs/CONFIGURATION.md)
- [API Documentation](docs/API.md)
- [Déploiement](docs/DEPLOYMENT.md)
- [Développement](docs/DEVELOPMENT.md)

## 🎯 Fonctionnalités

- ✅ **Catalogue de gâteaux** avec images
- ✅ **Système de commandes** avec WhatsApp
- ✅ **Dashboard patron/collaborateur**
- ✅ **Notifications temps réel**
- ✅ **Galerie photos**
- ✅ **Gestion des événements**
- ✅ **Paramètres de livraison**

## 🛠️ Technologies

- **Backend** : Django 5.1.6, DRF, Channels
- **Frontend** : React 19.1.0, Material-UI
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **Cache** : Redis (prod)
- **Déploiement** : Render, Gunicorn

## 📞 Support

Pour toute question ou problème, consultez la documentation dans le dossier `docs/`.

