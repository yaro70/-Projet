# 🔧 GUIDE DE DÉPANNAGE - ERREUR 403 LOGIN

## 🎯 PROBLÈME IDENTIFIÉ

Vous rencontrez une erreur 403 (Forbidden) lors de la connexion, mais le diagnostic montre que les serveurs fonctionnent correctement.

## ✅ DIAGNOSTIC EFFECTUÉ

- ✅ **Backend Django** : Fonctionnel (Status 200)
- ✅ **Frontend React** : Accessible (Status 200)  
- ✅ **Configuration CORS** : Correcte
- ✅ **API Login** : Opérationnelle
- ✅ **Headers CORS** : Présents

## 🔍 CAUSES POSSIBLES

### 1. **Cache du Navigateur**
Le navigateur utilise une ancienne version en cache.

### 2. **Variables d'Environnement**
Configuration React incorrecte.

### 3. **Configuration Réseau**
Problème de proxy ou de firewall.

## 🛠️ SOLUTIONS À ESSAYER

### **Solution 1: Nettoyage du Cache**

1. **Vider le cache du navigateur :**
   - Chrome/Edge : `Ctrl + Shift + R` ou `F12` → Network → "Disable cache"
   - Firefox : `Ctrl + Shift + R` ou `F12` → Network → "Disable cache"

2. **Navigation privée :**
   - Ouvrir une fenêtre de navigation privée
   - Tester la connexion

### **Solution 2: Redémarrage Propre**

```bash
# Arrêter tous les serveurs
pkill -f "python manage.py runserver"
pkill -f "react-scripts start"

# Nettoyer le cache React
cd frontend
rm -rf node_modules/.cache
rm -rf build
npm cache clean --force

# Redémarrer le backend
cd ../backend
source venv/bin/activate
python manage.py runserver &

# Redémarrer le frontend
cd ../frontend
npm start &
```

### **Solution 3: Vérification des Outils de Développement**

1. **Ouvrir F12** (Outils de développement)
2. **Onglet Network**
3. **Tenter la connexion**
4. **Vérifier la requête POST vers `/api/login/`**
5. **Regarder les headers de la requête et de la réponse**

### **Solution 4: Test Direct**

Tester directement l'API avec curl :

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"username": "admin", "password": "admin123"}'
```

## 🔑 IDENTIFIANTS DE TEST

| Rôle | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `admin123` |
| **Patron** | `patron` | `patron123` |
| **Collaborateur** | `collaborateur` | `collaborateur123` |

## 🌐 URLs D'ACCÈS

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000/api/
- **Admin Django** : http://localhost:8000/admin/

## 📊 ÉTAT ACTUEL DES SERVEURS

- ✅ **Backend Django** : Port 8000 - Fonctionnel
- ✅ **Frontend React** : Port 3000 - Accessible
- ✅ **Configuration CORS** : Correcte
- ✅ **Base de données** : Opérationnelle

## 🚨 SI LE PROBLÈME PERSISTE

1. **Vérifiez les logs du navigateur** (Console F12)
2. **Vérifiez les logs du serveur Django** (terminal backend)
3. **Testez avec un autre navigateur**
4. **Vérifiez les paramètres de proxy/firewall**

## 💡 CONSEIL

Le problème est très probablement lié au **cache du navigateur**. Essayez d'abord la **navigation privée** ou le **nettoyage du cache**.

---

**🎯 PROCHAINES ÉTAPES :**
1. Essayez la navigation privée
2. Si ça ne marche pas, nettoyez le cache
3. Si ça ne marche toujours pas, vérifiez les outils de développement
4. Reportez-moi les erreurs spécifiques que vous voyez
