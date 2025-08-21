# 🎂 Projet Pâtisserie - Déploiement Automatique

## 🚀 Déploiement Automatique sur Render

Ce projet est configuré pour un déploiement **100% automatique** sur Render.

### 📋 Prérequis

- Compte GitHub avec le code source
- Compte Render (gratuit)

### 🔄 Déploiement Automatique

1. **Allez sur** : https://dashboard.render.com
2. **Cliquez sur** "New" → "Blueprint"
3. **Connectez votre repository** GitHub
4. **Cliquez sur** "Connect Repository"
5. **Cliquez sur** "Apply"

**C'est tout !** Render va automatiquement :
- ✅ Déployer le backend Django
- ✅ Déployer le frontend React
- ✅ Configurer la base de données
- ✅ Créer les utilisateurs de test
- ✅ Configurer les URLs

### 🌐 URLs Générées

Après le déploiement, vous aurez :
- **Frontend** : `https://patisserie-frontend.onrender.com`
- **Backend** : `https://patisserie-backend.onrender.com`
- **Admin** : `https://patisserie-backend.onrender.com/admin/`

### 🔑 Identifiants de Test

| Rôle | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `admin123` |
| **Patron** | `patron` | `patron123` |
| **Collaborateur** | `collaborateur` | `collaborateur123` |

### 🎂 Fonctionnalités

- ✅ Catalogue des gâteaux
- ✅ Système de commande avec WhatsApp
- ✅ Dashboard patron et collaborateur
- ✅ Authentification complète
- ✅ Notifications en temps réel
- ✅ Gestion des articles et galerie

### 🔧 Configuration Technique

- **Backend** : Django 5.1.6 + Gunicorn
- **Frontend** : React 19.1.0 + Material-UI
- **Base de données** : PostgreSQL (Render)
- **Cache** : Redis (Render)
- **HTTPS** : Activé automatiquement

---

**🎉 Aucune configuration manuelle requise ! Le déploiement est entièrement automatique.** 