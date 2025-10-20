# 📡 API Documentation

## 🔗 Endpoints Principaux

### Base URL
```
http://localhost:8000/api/
```

## 🔐 Authentification

### Login
```http
POST /api/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

**Réponse :**
```json
{
    "token": "your-auth-token",
    "user": {
        "id": 1,
        "username": "admin",
        "is_patron": false,
        "is_collaborateur": false
    }
}
```

### Logout
```http
POST /api/logout/
Authorization: Token your-auth-token
```

## 🎂 Gâteaux

### Liste des gâteaux publics
```http
GET /api/public/gateaux/
```

**Réponse :**
```json
[
    {
        "id": 1,
        "nom": "Gâteau d'Anniversaire",
        "description": "Délicieux gâteau au chocolat",
        "prix": "15000.00",
        "image_url": "http://localhost:8000/media/gateaux/gateau.jpg",
        "disponible": true
    }
]
```

### Créer un gâteau (Admin)
```http
POST /api/gateaux/
Authorization: Token your-auth-token
Content-Type: application/json

{
    "nom": "Nouveau Gâteau",
    "description": "Description du gâteau",
    "prix": "20000.00",
    "type": "anniversaire",
    "disponible": true
}
```

## 📦 Commandes

### Créer une commande
```http
POST /api/commandes/
Content-Type: application/json

{
    "client_nom": "Jean Dupont",
    "client_telephone": "0123456789",
    "gateau": 1,
    "texte_sur_gateau": "Joyeux Anniversaire",
    "date_livraison": "2024-12-25T14:00:00Z",
    "livraison": true
}
```

### Liste des commandes (Authentifié)
```http
GET /api/commandes/
Authorization: Token your-auth-token
```

### Valider une commande
```http
PATCH /api/commandes/1/
Authorization: Token your-auth-token
Content-Type: application/json

{
    "status": "validee"
}
```

## 📸 Galerie

### Photos de la galerie
```http
GET /api/galerie/
```

**Paramètres :**
- `categorie` : Filtrer par catégorie (gateaux, evenements, ateliers, autres)
- `limit` : Limiter le nombre de résultats

### Ajouter une photo (Admin)
```http
POST /api/galerie/ajouter/
Authorization: Token your-auth-token
Content-Type: multipart/form-data

{
    "titre": "Mon Gâteau",
    "description": "Description de la photo",
    "image": <file>,
    "categorie": "gateaux",
    "date_realisation": "2024-01-01"
}
```

## 📰 Articles/Événements

### Liste des articles
```http
GET /api/articles/
```

### Créer un article (Admin)
```http
POST /api/articles/
Authorization: Token your-auth-token
Content-Type: application/json

{
    "titre": "Nouvel Événement",
    "contenu": "Contenu de l'article",
    "date_evenement": "2024-12-25T18:00:00Z",
    "actif": true
}
```

## 🔔 Notifications

### Notifications utilisateur
```http
GET /api/notifications/
Authorization: Token your-auth-token
```

### Marquer comme lu
```http
PATCH /api/notifications/1/marquer-lu/
Authorization: Token your-auth-token
```

## ⚙️ Paramètres

### Paramètres de livraison
```http
GET /api/parametres/
```

### Modifier les paramètres (Admin)
```http
PATCH /api/parametres/
Authorization: Token your-auth-token
Content-Type: application/json

{
    "prix_livraison": "2500.00"
}
```

## 🔌 WebSocket

### Connexion
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/notifications/');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Notification reçue:', data);
};
```

### Types de messages
- `new_order` : Nouvelle commande
- `order_validated` : Commande validée
- `order_finished` : Commande terminée
- `system_message` : Message système

## 📊 Codes de Statut

- `200` : Succès
- `201` : Créé
- `400` : Erreur de validation
- `401` : Non authentifié
- `403` : Non autorisé
- `404` : Non trouvé
- `500` : Erreur serveur

