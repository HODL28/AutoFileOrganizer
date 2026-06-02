# Règles de Développement

## 1. Simplicité maximale

- Favoriser la lisibilité.
- Éviter l'over-engineering.
- Pas de dépendance inutile.

## 2. Sécurité

- Ne jamais supprimer de fichiers.
- Déplacer uniquement.
- Vérifier les chemins avant action.

## 3. Robustesse

- Gérer toutes les erreurs.
- Messages utilisateur explicites.
- Aucun crash non intercepté.

## 4. Tests

- Chaque fonctionnalité critique doit être couverte.
- Aucun code non testé.

## 5. GitHub

- Commits atomiques.
- Messages de commit explicites.
- README maintenu à jour.

## 6. Open Source

- Code documenté.
- Type hints obligatoires.
- Docstrings obligatoires.

## 7. Performance

- Support de plusieurs milliers de fichiers.
- Éviter les scans redondants.

## 8. Interdictions

- Ne jamais modifier `document/`.
- Ne jamais modifier `cloud.md`.
- Ne jamais désactiver les tests.
