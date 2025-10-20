# 🚀 Guide de Déploiement

## 🌐 Déploiement sur Render (Recommandé)

### Option 1 : Déploiement Automatique avec Blueprint

1. **Connectez votre repository GitHub à Render**
2. **Créez un nouveau Blueprint**
3. **Sélectionnez le fichier `deploy/render.yaml`**
4. **Cliquez sur "Apply"**

Render va automatiquement :
- ✅ Déployer le backend Django
- ✅ Déployer le frontend React
- ✅ Configurer les URLs
- ✅ Créer les utilisateurs de test

### Option 2 : Déploiement Manuel

#### Backend Django
1. **Créez un nouveau Web Service**
2. **Configuration :**
   - **Build Command** : `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command** : `gunicorn patisserie_project.wsgi:application --bind 0.0.0.0:$PORT`
   - **Environment** : `python`
   - **Plan** : `free` ou `starter`

3. **Variables d'environnement :**
   ```
   DJANGO_SETTINGS_MODULE=patisserie_project.settings_render
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   ```

#### Frontend React
1. **Créez un nouveau Static Site**
2. **Configuration :**
   - **Build Command** : `cd frontend && npm install && npm run build`
   - **Publish Directory** : `frontend/build`
   - **Environment** : `node`
   - **Plan** : `free`

3. **Variables d'environnement :**
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   REACT_APP_WS_URL=wss://your-backend.onrender.com
   ```

## 🐳 Déploiement avec Docker

### Dockerfile Backend
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
EXPOSE 8000

CMD ["gunicorn", "patisserie_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Dockerfile Frontend
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:pass@db:5432/patisserie
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=patisserie
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔧 Configuration Production

### Variables d'Environnement
```bash
# Backend
SECRET_KEY=your-super-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Cache (Redis)
CACHE_URL=redis://redis:6379/1
CHANNEL_LAYERS_BACKEND=channels_redis.core.RedisChannelLayer

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_WS_URL=wss://api.yourdomain.com
```

### Sécurité
```python
# settings_production.py
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📊 Monitoring

### Logs
- **Render** : Dashboard → Logs
- **Docker** : `docker logs container_name`

### Health Check
```python
# urls.py
urlpatterns = [
    path('health/', lambda r: HttpResponse('OK')),
    # ...
]
```

## 🔄 Mise à Jour

### Render
1. **Push** vos modifications sur GitHub
2. **Render** redéploie automatiquement

### Docker
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

## 🆘 Dépannage

### Erreurs Communes

**502 Bad Gateway**
- Vérifiez que le serveur démarre correctement
- Vérifiez les logs dans Render

**CORS Errors**
- Vérifiez `CORS_ALLOWED_ORIGINS`
- Ajoutez votre domaine frontend

**Database Errors**
- Vérifiez `DATABASE_URL`
- Exécutez les migrations : `python manage.py migrate`

**Static Files 404**
- Vérifiez `STATIC_ROOT` et `STATIC_URL`
- Exécutez `python manage.py collectstatic`

