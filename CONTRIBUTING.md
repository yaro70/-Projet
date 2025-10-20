# 🤝 Guide de Contribution

## 📋 Comment Contribuer

Merci de votre intérêt à contribuer au Projet Pâtisserie ! Voici comment vous pouvez nous aider.

## 🚀 Démarrage Rapide

### 1. Fork et Clone
```bash
# Fork le repository sur GitHub
# Puis clonez votre fork
git clone https://github.com/votre-username/patisserie_project.git
cd patisserie_project
```

### 2. Configuration
```bash
# Configuration automatique
python scripts/setup.py
```

### 3. Développement
```bash
# Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Frontend (nouveau terminal)
cd frontend
npm start
```

## 📝 Types de Contributions

### 🐛 Bug Reports
- Utilisez le template de bug report
- Incluez les étapes pour reproduire
- Ajoutez des logs d'erreur si possible

### ✨ Nouvelles Fonctionnalités
- Ouvrez une issue pour discuter de la fonctionnalité
- Créez une branche feature
- Ajoutez des tests
- Mettez à jour la documentation

### 📚 Documentation
- Améliorez les guides existants
- Ajoutez des exemples
- Corrigez les erreurs

### 🧪 Tests
- Ajoutez des tests unitaires
- Améliorez la couverture de code
- Testez sur différents navigateurs

## 🔄 Workflow de Contribution

### 1. Créer une Branche
```bash
git checkout -b feature/nom-de-la-fonctionnalite
# ou
git checkout -b bugfix/nom-du-bug
```

### 2. Développer
- Codez votre fonctionnalité
- Ajoutez des tests
- Mettez à jour la documentation

### 3. Tester
```bash
# Backend
cd backend
python manage.py test

# Frontend
cd frontend
npm test
```

### 4. Commit
```bash
git add .
git commit -m "feat: ajouter nouvelle fonctionnalité"
# ou
git commit -m "fix: corriger bug dans le système de commandes"
```

### 5. Push et Pull Request
```bash
git push origin feature/nom-de-la-fonctionnalite
```

Puis créez une Pull Request sur GitHub.

## 📏 Standards de Code

### Python/Django
- Suivez PEP 8
- Utilisez des docstrings
- Nommez les variables clairement
- Ajoutez des commentaires pour la logique complexe

### JavaScript/React
- Utilisez ESLint
- Suivez les conventions React
- Nommez les composants en PascalCase
- Utilisez des hooks plutôt que des classes

### Git
- Messages de commit clairs
- Utilisez le format conventional commits
- Une fonctionnalité par commit

## 🧪 Tests

### Backend
```bash
cd backend
python manage.py test boutique
```

### Frontend
```bash
cd frontend
npm test
```

### Tests E2E
```bash
# À implémenter avec Cypress ou Playwright
```

## 📚 Documentation

### Backend
- Docstrings pour toutes les fonctions
- Documentation des modèles
- Exemples d'utilisation des APIs

### Frontend
- JSDoc pour les fonctions complexes
- Documentation des composants
- Exemples d'utilisation

## 🔍 Code Review

### Critères d'Acceptation
- [ ] Code fonctionne correctement
- [ ] Tests passent
- [ ] Documentation mise à jour
- [ ] Pas de régression
- [ ] Code lisible et maintenable

### Checklist du Reviewer
- [ ] Fonctionnalité testée
- [ ] Code reviewé ligne par ligne
- [ ] Tests vérifiés
- [ ] Documentation vérifiée
- [ ] Performance acceptable

## 🐛 Reporting de Bugs

### Template de Bug Report
```markdown
## Description
Description claire du bug

## Étapes pour Reproduire
1. Aller à '...'
2. Cliquer sur '...'
3. Voir l'erreur

## Comportement Attendu
Ce qui devrait se passer

## Comportement Actuel
Ce qui se passe réellement

## Environnement
- OS: [ex: Windows 10]
- Navigateur: [ex: Chrome 91]
- Version: [ex: 1.0.0]

## Logs
Ajoutez les logs d'erreur si disponibles
```

## ✨ Proposer une Fonctionnalité

### Template de Feature Request
```markdown
## Description
Description claire de la fonctionnalité

## Problème Résolu
Quel problème cette fonctionnalité résout-elle ?

## Solution Proposée
Description de la solution

## Alternatives
Autres solutions considérées

## Contexte Additionnel
Toute autre information utile
```

## 📞 Support

- **Issues** : Pour les bugs et demandes de fonctionnalités
- **Discussions** : Pour les questions générales
- **Email** : Pour les questions privées

## 📜 Licence

En contribuant, vous acceptez que vos contributions soient sous la même licence que le projet.

## 🙏 Remerciements

Merci à tous les contributeurs qui rendent ce projet possible !

---

**N'hésitez pas à poser des questions si vous avez besoin d'aide !** 🚀

