# ⚙️ Configuration

## 🔧 Variables d'Environnement

### Backend (Django)

```bash
# Fichier .env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Channels (WebSocket)
CHANNEL_LAYERS_BACKEND=channels.layers.InMemoryChannelLayer

# Cache
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
```

### Frontend (React)

```bash
# Fichier .env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

## 🗄️ Base de Données

### SQLite (Développement)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL (Production)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'patisserie_db',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔐 Sécurité

### Production
```python
# Sécurité HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies sécurisés
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### CORS
```python
# Autoriser seulement les domaines spécifiques
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## 📱 WhatsApp Configuration

Modifiez le numéro de téléphone dans `boutique/models.py` :

```python
def get_whatsapp_link(self):
    # Remplacez par votre numéro
    return f"https://wa.me/2250123456789?text={encoded_message}"
```

## 🖼️ Gestion des Images

### Pillow (Optionnel)
```bash
pip install Pillow
```

### Configuration
```python
# Redimensionnement automatique
MAX_IMAGE_SIZE = (500, 500)
UPLOAD_TO = 'media/'
```

## 🔔 Notifications

### Types de Notifications
- `new_order` : Nouvelle commande
- `order_validated` : Commande validée
- `order_finished` : Commande terminée
- `system_message` : Message système

### Configuration WebSocket
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        # Ou Redis pour la production
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
    },
}
```

