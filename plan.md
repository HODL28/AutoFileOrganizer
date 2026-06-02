# AutoFileOrganizer - Plan d'Implémentation

## Objectif

Créer un outil open source Python permettant d'organiser automatiquement les fichiers d'un dossier selon leur type.

Le projet doit être publiable sur GitHub et installable via pip.

---

# Phase 1 - Initialisation

- Python 3.12+
- Typer (CLI)
- Rich (affichage terminal)
- Pytest
- Ruff
- GitHub Actions CI

Structure :

```
autofileorganizer/
│
├── src/autofileorganizer/
│   ├── cli.py
│   ├── organizer.py
│   ├── scanner.py
│   ├── categories.py
│   ├── report.py
│   └── utils.py
│
├── tests/
├── screenshots/
├── docs/
├── README.md
├── LICENSE
├── pyproject.toml
└── .github/workflows/ci.yml
```

---

# Phase 2 - Détection des catégories

Catégories :

**Images**
- jpg
- jpeg
- png
- gif
- webp
- svg

**Vidéos**
- mp4
- mov
- avi
- mkv

**Documents**
- pdf
- docx
- doc
- xlsx
- pptx
- txt

**Musique**
- mp3
- wav
- flac

**Archives**
- zip
- rar
- 7z
- tar
- gz

**Code**
- py
- js
- ts
- jsx
- tsx
- html
- css
- java
- cpp
- c
- go
- rs

**Autres**
- tout le reste

---

# Phase 3 - Scanner

Créer un scanner :

Entrées :
- dossier cible
- mode récursif

Sorties :
- liste complète des fichiers

Exclure :
- dossiers système
- liens symboliques dangereux

---

# Phase 4 - Dry Run

Commande :

```
organize --dry-run
```

Afficher :

```
SOURCE → DESTINATION
```

Aucune modification disque.

---

# Phase 5 - Déplacement

Commande :

```
organize
```

Créer automatiquement les dossiers :

```
Images/
Videos/
Documents/
Music/
Archives/
Code/
Others/
```

Déplacer les fichiers.

Gérer les conflits :

```
fichier.txt
fichier_1.txt
fichier_2.txt
```

---

# Phase 6 - Rapport

Afficher un tableau Rich :

| Catégorie | Nb fichiers | Destination |
|-----------|------------|-------------|

Afficher :

- nombre total analysé
- nombre déplacé
- durée d'exécution

---

# Phase 7 - CLI

Commandes :

```bash
organize

organize "C:/Downloads"

organize --recursive

organize --dry-run

organize --help
```

---

# Phase 8 - Tests

Tests unitaires :

- catégorisation
- renommage
- scan
- dry-run
- déplacement

Couverture minimum : **90%**

---

# Phase 9 - GitHub

Créer automatiquement :

**README professionnel**

Sections :

- Description
- Fonctionnalités
- Installation
- Utilisation
- Exemples
- Captures écran
- Contribution
- Licence

Créer **LICENSE MIT**.

Créer release **v1.0.0**.

Configurer **GitHub Actions** :

- lint
- tests

---

# Phase 10 - Publication

Créer dépôt GitHub public.

Push complet du projet.

Créer tags :

```
v1.0.0
```

Projet prêt pour open source.
