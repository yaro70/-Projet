# 👨‍💻 Guide de Développement

## 🏗️ Architecture du Projet

```
patisserie_project/
├── backend/                    # API Django
│   ├── boutique/              # Application principale
│   │   ├── models.py         # Modèles de données
│   │   ├── views.py          # Vues API
│   │   ├── serializers.py    # Sérialiseurs DRF
│   │   ├── admin.py         # Interface admin
│   │   ├── consumers.py    # WebSocket consumers
│   │   └── routing.py      # Routes WebSocket
│   ├── patisserie_project/  # Configuration Django
│   │   ├── settings.py     # Settings développement
│   │   ├── settings_render.py # Settings production
│   │   ├── urls.py         # URLs principales
│   │   ├── asgi.py         # Configuration ASGI
│   │   └── wsgi.py         # Configuration WSGI
│   └── manage.py
├── frontend/                  # Interface React
│   ├── src/
│   │   ├── components/      # Composants React
│   │   │   ├── AuthContext.js
│   │   │   ├── Catalogue.js
│   │   │   ├── Commande.js
│   │   │   ├── DashboardPatron.js
│   │   │   ├── DashboardCollaborateur.js
│   │   │   ├── Galerie.js
│   │   │   ├── Home.js
│   │   │   ├── Login.js
│   │   │   └── NotificationSystem.js
│   │   ├── config.js        # Configuration API
│   │   └── App.js           # Application principale
│   └── package.json
├── docs/                     # Documentation
├── scripts/                 # Scripts utilitaires
├── deploy/                  # Configuration déploiement
└── README.md
```

## 🔧 Configuration Développement

### Backend
```bash
# Environnement virtuel
python -m venv venv
source venv/bin/activate

# Dépendances
pip install -r requirements.txt

# Base de données
python manage.py migrate

# Serveur de développement
python manage.py runserver
```

### Frontend
```bash
# Dépendances
npm install

# Serveur de développement
npm start
```

## 📝 Modèles de Données

### User (Utilisateur)
```python
class User(AbstractUser):
    is_patron = models.BooleanField(default=False)
    is_collaborateur = models.BooleanField(default=False)
```

### Gateau (Gâteau)
```python
class Gateau(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='gateaux/')
    disponible = models.BooleanField(default=True)
```

### Commande
```python
class Commande(models.Model):
    client_nom = models.CharField(max_length=100)
    client_telephone = models.CharField(max_length=20)
    gateau = models.ForeignKey(Gateau, on_delete=models.CASCADE)
    texte_sur_gateau = models.CharField(max_length=100)
    date_livraison = models.DateTimeField()
    livraison = models.BooleanField(default=False)
    prix_total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
```

## 🔌 API Endpoints

### Authentification
- `POST /api/login/` - Connexion
- `POST /api/logout/` - Déconnexion

### Gâteaux
- `GET /api/public/gateaux/` - Liste publique
- `GET /api/gateaux/` - Liste (authentifié)
- `POST /api/gateaux/` - Créer (admin)

### Commandes
- `POST /api/commandes/` - Créer commande
- `GET /api/commandes/` - Liste (authentifié)
- `PATCH /api/commandes/{id}/` - Modifier statut

### Galerie
- `GET /api/galerie/` - Photos publiques
- `POST /api/galerie/ajouter/` - Ajouter photo (admin)

## 🔔 WebSocket

### Connexion
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/notifications/');
```

### Types de Messages
- `new_order` : Nouvelle commande
- `order_validated` : Commande validée
- `order_finished` : Commande terminée
- `system_message` : Message système

## 🧪 Tests

### Backend
```bash
python manage.py test
```

### Frontend
```bash
npm test
```

## 📦 Ajout de Fonctionnalités

### 1. Nouveau Modèle
```python
# boutique/models.py
class NouveauModele(models.Model):
    nom = models.CharField(max_length=100)
    # ...

# Créer migration
python manage.py makemigrations boutique

# Appliquer migration
python manage.py migrate
```

### 2. Nouvelle API
```python
# boutique/views.py
class NouveauViewSet(viewsets.ModelViewSet):
    queryset = NouveauModele.objects.all()
    serializer_class = NouveauSerializer
```

### 3. Nouveau Composant React
```javascript
// frontend/src/components/NouveauComposant.js
import React from 'react';

const NouveauComposant = () => {
    return <div>Nouveau Composant</div>;
};

export default NouveauComposant;
```

## 🔍 Debugging

### Backend
```python
# Ajouter des logs
import logging
logger = logging.getLogger(__name__)

def ma_fonction():
    logger.info("Message de debug")
```

### Frontend
```javascript
// Console logs
console.log("Debug:", data);

// React DevTools
// Installer l'extension navigateur
```

## 📊 Performance

### Backend
- Utilisez `select_related()` et `prefetch_related()`
- Mettez en cache les requêtes fréquentes
- Optimisez les requêtes avec `only()` et `defer()`

### Frontend
- Utilisez `React.memo()` pour les composants
- Implémentez le lazy loading
- Optimisez les images

## 🔒 Sécurité

### Backend
- Validez toujours les données d'entrée
- Utilisez les permissions DRF
- Protégez contre les attaques CSRF

### Frontend
- Ne stockez jamais de données sensibles
- Validez les données côté client
- Utilisez HTTPS en production

