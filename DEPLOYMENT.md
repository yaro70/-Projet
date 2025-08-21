# 🚀 Guide de Déploiement sur Render

Ce guide vous accompagne pour déployer votre application de pâtisserie sur Render.

## 📋 Prérequis

- Compte Render (gratuit)
- Projet Git (GitHub, GitLab, etc.)
- Base de données PostgreSQL (fournie par Render)
- Service Redis (fourni par Render)

## 🎯 Architecture de Déploiement

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Base de       │
│   React         │◄──►│   Django        │◄──►│   Données       │
│   (Static)      │    │   (Web Service) │    │   PostgreSQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Redis         │
                       │   (Cache/WS)    │
                       └─────────────────┘
```

## 🔧 Étape 1 : Préparation du Code

### 1.1 Vérifier les fichiers de configuration

Assurez-vous que ces fichiers sont présents :
- ✅ `requirements.txt` - Dépendances Python
- ✅ `patisserie_project/settings_production.py` - Configuration production
- ✅ `build.sh` - Script de build
- ✅ `render.yaml` - Configuration Render
- ✅ `frontend/src/config.js` - Configuration frontend

### 1.2 Pousser le code sur Git

```bash
git add .
git commit -m "Préparation pour déploiement Render"
git push origin main
```

## 🌐 Étape 2 : Configuration Render

### 2.1 Créer un compte Render

1. Allez sur [render.com](https://render.com)
2. Créez un compte gratuit
3. Connectez votre repository Git

### 2.2 Déployer avec render.yaml (Recommandé)

1. **Connecter le repository** :
   - Cliquez sur "New +"
   - Sélectionnez "Blueprint"
   - Connectez votre repository Git

2. **Render détectera automatiquement** `render.yaml` et créera :
   - Service backend Django
   - Service frontend React
   - Base de données PostgreSQL
   - Service Redis

### 2.3 Configuration manuelle (Alternative)

Si vous préférez configurer manuellement :

#### Service Backend Django

1. **Nouveau Web Service** :
   - Name: `patisserie-backend`
   - Environment: `Python 3`
   - Build Command: `chmod +x build.sh && ./build.sh`
   - Start Command: `gunicorn patisserie_project.wsgi:application --bind 0.0.0.0:$PORT`

2. **Variables d'environnement** :
   ```
   DJANGO_SETTINGS_MODULE=patisserie_project.settings_production
   SECRET_KEY=<généré automatiquement>
   DEBUG=false
   ALLOWED_HOSTS=.onrender.com
   ```

3. **Base de données** :
   - Créez une base PostgreSQL
   - Render fournira automatiquement `DATABASE_URL`

4. **Redis** :
   - Créez un service Redis
   - Render fournira automatiquement `REDIS_URL`

#### Service Frontend React

1. **Nouveau Static Site** :
   - Name: `patisserie-frontend`
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/build`

2. **Variables d'environnement** :
   ```
   REACT_APP_API_URL=https://patisserie-backend.onrender.com
   REACT_APP_WS_URL=wss://patisserie-backend.onrender.com
   ```

## 🔗 Étape 3 : Configuration des URLs

### 3.1 Mettre à jour CORS

Une fois déployé, mettez à jour `CORS_ALLOWED_ORIGINS` dans Render :

```
https://patisserie-frontend.onrender.com,http://localhost:3000
```

### 3.2 Mettre à jour les URLs frontend

Dans les variables d'environnement du frontend :

```
REACT_APP_API_URL=https://patisserie-backend.onrender.com
REACT_APP_WS_URL=wss://patisserie-backend.onrender.com
```

## 🗄️ Étape 4 : Base de Données

### 4.1 Migration automatique

Le script `build.sh` exécute automatiquement :
```bash
python manage.py migrate
```

### 4.2 Création des données initiales

Après le premier déploiement, connectez-vous au shell Render :

```bash
# Dans le dashboard Render, allez dans votre service backend
# Cliquez sur "Shell" et exécutez :

python manage.py shell
```

```python
# Créer un superuser
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

# Créer des données de test
exec(open('create_test_data.py').read())
```

## 🔐 Étape 5 : Sécurité

### 5.1 Variables d'environnement sensibles

Render génère automatiquement :
- ✅ `SECRET_KEY` - Clé secrète Django
- ✅ `DATABASE_URL` - Connexion PostgreSQL
- ✅ `REDIS_URL` - Connexion Redis

### 5.2 HTTPS automatique

Render fournit automatiquement :
- ✅ Certificats SSL
- ✅ Redirection HTTPS
- ✅ Headers de sécurité

## 📊 Étape 6 : Monitoring

### 6.1 Logs

Dans le dashboard Render :
- **Logs** : Voir les logs en temps réel
- **Metrics** : Performance et utilisation
- **Health Checks** : Vérification automatique

### 6.2 Déploiements automatiques

- ✅ Déploiement automatique à chaque push
- ✅ Rollback en un clic
- ✅ Preview deployments

## 🚨 Dépannage

### Problème : Build échoue

**Solution** :
1. Vérifiez les logs dans Render
2. Testez localement : `./build.sh`
3. Vérifiez `requirements.txt`

### Problème : Erreur de base de données

**Solution** :
1. Vérifiez `DATABASE_URL` dans les variables d'environnement
2. Exécutez manuellement : `python manage.py migrate`
3. Vérifiez la connexion PostgreSQL

### Problème : CORS errors

**Solution** :
1. Mettez à jour `CORS_ALLOWED_ORIGINS`
2. Vérifiez les URLs frontend/backend
3. Redéployez après modification

### Problème : WebSocket ne fonctionne pas

**Solution** :
1. Vérifiez `REDIS_URL`
2. Assurez-vous que Redis est connecté
3. Vérifiez les logs WebSocket

## 📱 URLs Finales

Après déploiement, vos URLs seront :

- **Frontend** : `https://patisserie-frontend.onrender.com`
- **Backend API** : `https://patisserie-backend.onrender.com`
- **Admin Django** : `https://patisserie-backend.onrender.com/admin/`

## 🎉 Félicitations !

Votre application de pâtisserie est maintenant déployée sur Render avec :
- ✅ Backend Django sécurisé
- ✅ Frontend React optimisé
- ✅ Base de données PostgreSQL
- ✅ Cache Redis
- ✅ HTTPS automatique
- ✅ Déploiements automatiques

## 📞 Support

- **Documentation Render** : [docs.render.com](https://docs.render.com)
- **Logs d'erreur** : Dashboard Render → Service → Logs
- **Support communautaire** : [Render Community](https://community.render.com)

