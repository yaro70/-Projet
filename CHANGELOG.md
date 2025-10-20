# 📝 Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Structure de projet réorganisée et professionnalisée
- Documentation complète dans le dossier `docs/`
- Scripts d'installation et de déploiement automatisés
- Configuration d'environnement standardisée
- Guide de contribution pour les développeurs

### Changed
- Réorganisation complète de l'architecture des fichiers
- Séparation claire entre backend et frontend
- Amélioration de la documentation
- Standardisation des configurations

### Fixed
- Problèmes de déploiement sur Render
- Configuration des chemins Django
- Nettoyage des fichiers redondants

## [1.0.0] - 2024-01-XX

### Added
- 🎂 Système de gestion de pâtisserie complet
- 🔐 Authentification utilisateur avec rôles (Admin, Patron, Collaborateur)
- 📦 Catalogue de gâteaux avec images
- 🛒 Système de commandes avec intégration WhatsApp
- 📊 Dashboards pour patron et collaborateur
- 🔔 Notifications en temps réel avec WebSocket
- 📸 Galerie photos des réalisations
- 📰 Gestion des articles et événements
- ⚙️ Paramètres de livraison configurables
- 🌐 API REST complète avec Django REST Framework
- 🎨 Interface utilisateur moderne avec React et Material-UI
- 🚀 Déploiement automatisé sur Render
- 📱 Design responsive pour mobile et desktop

### Technical Details
- **Backend** : Django 5.1.6 + Django REST Framework + Django Channels
- **Frontend** : React 19.1.0 + Material-UI + Axios
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Cache** : LocMemCache (développement) / Redis (production)
- **WebSocket** : Django Channels avec InMemoryChannelLayer
- **Déploiement** : Render avec Gunicorn
- **Images** : Support Pillow avec redimensionnement automatique

### Features
- ✅ Authentification complète avec tokens
- ✅ Gestion des utilisateurs avec rôles
- ✅ Catalogue de gâteaux avec images
- ✅ Système de commandes avec statuts
- ✅ Intégration WhatsApp pour notifications
- ✅ Dashboards personnalisés par rôle
- ✅ Notifications temps réel
- ✅ Galerie photos avec catégories
- ✅ Gestion des événements
- ✅ Paramètres de livraison
- ✅ Interface d'administration Django
- ✅ API REST documentée
- ✅ Design responsive
- ✅ Déploiement automatisé

### Security
- 🔒 Authentification par token
- 🛡️ Permissions basées sur les rôles
- 🔐 Validation des données
- 🌐 Configuration CORS sécurisée
- 🔒 Headers de sécurité HTTPS

### Performance
- ⚡ Cache des requêtes fréquentes
- 🖼️ Optimisation des images
- 📦 Lazy loading des composants
- 🗄️ Optimisation des requêtes de base de données
- 📊 Pagination des listes

---

## Types de Changements

- **Added** : Nouvelles fonctionnalités
- **Changed** : Changements dans les fonctionnalités existantes
- **Deprecated** : Fonctionnalités qui seront supprimées
- **Removed** : Fonctionnalités supprimées
- **Fixed** : Corrections de bugs
- **Security** : Corrections de vulnérabilités

