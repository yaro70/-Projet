# 🚀 Guide d'Installation

## 📋 Prérequis

- Python 3.11+
- Node.js 18+
- Git

## 🔧 Installation Backend

```bash
# Cloner le projet
git clone <repository-url>
cd patisserie_project/backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver
```

## 🎨 Installation Frontend

```bash
# Dans un nouveau terminal
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm start
```

## 🌐 Accès

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000/api/
- **Admin Django** : http://localhost:8000/admin/

## 🧪 Données de Test

Le système crée automatiquement :
- 3 gâteaux d'exemple
- Utilisateurs de test (patron, collaborateur)
- Paramètres de livraison

## 🔧 Configuration

Copiez `env.example` vers `.env` et configurez vos variables :

```bash
cp env.example .env
```

Variables importantes :
- `SECRET_KEY` : Clé secrète Django
- `DEBUG` : Mode debug (True/False)
- `DATABASE_URL` : URL de la base de données

