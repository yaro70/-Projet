# 🎂 Projet Pâtisserie - Application Web

Une application web complète pour la gestion d'une pâtisserie avec système d'authentification, gestion des commandes et catalogue de gâteaux.

## 🚀 Fonctionnalités

### 👥 Rôles utilisateurs
- **Patron** : Gestion complète (commandes, gâteaux, paramètres)
- **Collaborateur** : Traitement des commandes
- **Client** : Consultation du catalogue et passation de commandes

### 📋 Fonctionnalités principales
- ✅ Authentification sécurisée
- ✅ Catalogue de gâteaux
- ✅ Système de commandes
- ✅ Gestion des statuts de commandes
- ✅ Paramètres de livraison
- ✅ Interface responsive
- ✅ Notifications en temps réel
- ✅ Galerie photos
- ✅ Système WhatsApp intégré
- ✅ Statistiques et rapports

## 🛠️ Technologies utilisées

### Backend
- **Django 5.1.6** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de données (production)
- **Redis** - Cache et WebSocket (production)
- **Django Channels** - Notifications temps réel
- **Gunicorn** - Serveur WSGI (production)

### Frontend
- **React 19** - Interface utilisateur
- **Material-UI** - Composants UI
- **Axios** - Requêtes HTTP
- **React Router** - Navigation
- **WebSocket** - Notifications temps réel

## 🚀 Déploiement Rapide

### Option 1 : Déploiement automatique sur Render

1. **Forkez ce repository** sur GitHub
2. **Connectez-vous sur [Render.com](https://render.com)**
3. **Cliquez sur "New +" → "Blueprint"**
4. **Connectez votre repository**
5. **Render déploiera automatiquement** :
   - Backend Django
   - Frontend React
   - Base de données PostgreSQL
   - Cache Redis

### Option 2 : Installation locale

#### Prérequis
- Python 3.8+
- Node.js 16+
- npm ou yarn

#### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd patisserie_project
```

#### 2. Configuration Backend (Django)

##### Activer l'environnement virtuel
```bash
cd ..
source env/bin/activate
cd patisserie_project
```

##### Installer les dépendances
```bash
pip install -r requirements.txt
```

##### Exécuter les migrations
```bash
python manage.py migrate
```

##### Créer les données de test
```bash
python create_test_data.py
```

##### Créer les utilisateurs de test
```bash
python set_passwords.py
python create_test_user.py
```

##### Démarrer le serveur Django
```bash
python manage.py runserver 8000
```

#### 3. Configuration Frontend (React)

##### Installer les dépendances
```bash
cd frontend
npm install
```

##### Démarrer le serveur de développement
```bash
npm start
```

## 🔑 Identifiants de test

### Utilisateurs existants
- **Patron** : `deliceDek@ty` / `delicedek@ty123`
- **Patron** : `T0T01234` / `t0t01234123`
- **Client** : `YARO` / `yaro123`

### Utilisateur de test
- **Patron** : `test` / `test123`

## 📁 Structure du projet

```
patisserie_project/
├── boutique/                 # Application Django principale
│   ├── models.py            # Modèles de données
│   ├── views.py             # Vues API
│   ├── serializers.py       # Sérialiseurs
│   ├── consumers.py         # WebSocket consumers
│   ├── routing.py           # WebSocket routing
│   └── admin.py             # Interface d'administration
├── frontend/                # Application React
│   ├── src/
│   │   ├── components/      # Composants React
│   │   ├── config.js        # Configuration centralisée
│   │   └── App.js          # Application principale
│   └── package.json
├── patisserie_project/      # Configuration Django
│   ├── settings.py         # Paramètres développement
│   ├── settings_production.py # Paramètres production
│   ├── asgi.py             # Configuration ASGI
│   └── urls.py             # URLs principales
├── build.sh                # Script de build Render
├── render.yaml             # Configuration Render
├── requirements.txt         # Dépendances Python
└── DEPLOYMENT.md           # Guide de déploiement complet
```

## 🔧 Configuration

### Variables d'environnement
Le projet utilise les paramètres par défaut de Django. Pour la production, configurez :
- `SECRET_KEY`
- `DEBUG = False`
- `ALLOWED_HOSTS`
- `DATABASE_URL` (PostgreSQL)
- `REDIS_URL` (Redis)

### CORS
Configuré pour permettre les requêtes depuis `http://localhost:3000` et les domaines Render

## 🚀 Déploiement

### Backend (Django)
```bash
python manage.py collectstatic
python manage.py migrate
gunicorn patisserie_project.wsgi:application
```

### Frontend (React)
```bash
npm run build
```

## 📝 API Endpoints

### Authentification
- `POST /api/login/` - Connexion
- `POST /api/logout/` - Déconnexion

### Gâteaux
- `GET /api/gateaux/` - Liste des gâteaux
- `GET /api/public/gateaux/` - Gâteaux publics
- `POST /api/gateaux/` - Créer un gâteau (patron)

### Commandes
- `GET /api/commandes/` - Liste des commandes
- `POST /api/create-commande/` - Créer une commande
- `PATCH /api/commandes/{id}/` - Modifier le statut
- `POST /api/commandes/{id}/mark-terminee/` - Marquer comme terminée

### Paramètres
- `GET /api/parametres/` - Paramètres de livraison
- `PUT /api/parametres/{id}/` - Modifier les paramètres (patron)

### Notifications
- `GET /api/notifications/` - Récupérer les notifications
- `POST /api/notifications/mark-read/` - Marquer comme lue
- `POST /api/notifications/mark-all-read/` - Tout marquer comme lu

### Galerie
- `GET /api/galerie/` - Photos de la galerie
- `POST /api/galerie/ajouter/` - Ajouter une photo (patron)
- `PUT /api/galerie/{id}/modifier/` - Modifier une photo (patron)
- `DELETE /api/galerie/{id}/supprimer/` - Supprimer une photo (patron)

### Gestion
- `POST /api/create-collaborateur/` - Créer un collaborateur (patron)
- `GET /api/statistiques/` - Statistiques (patron)
- `POST /api/create-article/` - Créer un article (patron)

## 🐛 Dépannage

### Problème de connexion
1. Vérifier que l'environnement virtuel est activé
2. Exécuter `python set_passwords.py`
3. Vérifier que le serveur Django fonctionne sur le port 8000

### Problème CORS
1. Vérifier la configuration dans `settings.py`
2. S'assurer que `django-cors-headers` est installé

### Problème de base de données
1. Exécuter `python manage.py migrate`
2. Vérifier les migrations avec `python manage.py showmigrations`

### Problème de déploiement
Consultez le guide complet : [DEPLOYMENT.md](DEPLOYMENT.md)

## 📞 Support

Pour toute question ou problème :
- **Documentation Render** : [docs.render.com](https://docs.render.com)
- **Guide de déploiement** : [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues GitHub** : Créez une issue sur le repository

## 📄 Licence

Ce projet est sous licence MIT. 