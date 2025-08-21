# 🔧 Configuration Manuelle Render

## 🚨 Problème Actuel
Render utilise `gunicorn app:app` au lieu de `gunicorn patisserie_project.wsgi:application`

## ✅ Solution : Configuration Manuelle

### **1. Dans Render Dashboard**

1. **Allez dans votre service backend**
2. **Cliquez sur "Settings"**
3. **Modifiez la "Start Command"** :

```
gunicorn patisserie_project.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
```

### **2. Variables d'Environnement**

Dans "Environment Variables", ajoutez :

| Variable | Valeur |
|----------|--------|
| `DJANGO_SETTINGS_MODULE` | `patisserie_project.settings_render` |
| `DEBUG` | `false` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `SECRET_KEY` | `[généré automatiquement]` |

### **3. Base de Données**

1. **Créez une base PostgreSQL** :
   - Type : PostgreSQL
   - Plan : Free
   - Nom : `patisserie-db`

2. **Connectez-la à votre service backend**

### **4. Redis (Optionnel)**

1. **Créez un service Redis** :
   - Type : Redis
   - Plan : Free
   - Nom : `patisserie-redis`

2. **Connectez-le à votre service backend**

### **5. Redéployez**

1. **Cliquez sur "Manual Deploy"**
2. **Sélectionnez "Deploy latest commit"**

## 🔄 Alternative : Nouveau Service avec Blueprint

Si la configuration manuelle ne fonctionne pas :

1. **Supprimez le service actuel**
2. **Créez un nouveau service** :
   - Type : Blueprint
   - Connectez votre repository
   - Render utilisera automatiquement `render.yaml`

## 📋 Commandes de Démarrage Alternatives

Si la commande principale ne fonctionne pas, essayez :

### **Option 1 : Script de démarrage**
```
./start.sh
```

### **Option 2 : Commande directe**
```
gunicorn patisserie_project.wsgi:application --bind 0.0.0.0:$PORT
```

### **Option 3 : Avec workers**
```
gunicorn patisserie_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2
```

## 🐛 Dépannage

### **Erreur : ModuleNotFoundError**
- Vérifiez que `DJANGO_SETTINGS_MODULE` est correct
- Assurez-vous que le chemin vers `wsgi.py` est bon

### **Erreur : ImportError**
- Vérifiez que toutes les dépendances sont installées
- Regardez les logs de build

### **Erreur : Database connection**
- Vérifiez que la base PostgreSQL est connectée
- Vérifiez `DATABASE_URL` dans les variables d'environnement

## 📞 Support

Si vous avez des problèmes :
1. Vérifiez les logs dans Render Dashboard
2. Testez localement avec : `python manage.py runserver`
3. Vérifiez la configuration avec : `python test_render_config.py`
