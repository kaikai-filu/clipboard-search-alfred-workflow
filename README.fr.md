# Recherche de presse-papiers · Clipboard Search for Alfred

Un workflow de recherche avancée dans l'historique du presse-papiers pour Alfred 5 (nécessite Powerpack).

Allez au-delà du visualiseur de presse-papiers intégré d'Alfred — recherchez et filtrez des milliers d'entrées par mot-clé, type, horaire, date et application source.

---

## Fonctionnalités

- **Recherche par mot-clé** — recherche plein texte dans l'historique
- **Filtres par type** — `:text` `:image` `:file`
- **Filtres temporels** — `:today` `:yesterday` `:2h` `:30m` `:3d`
- **Filtres par date** — `:2026-05-10` `:05-10` (année optionnelle) ou plages
- **Filtres par application** — `@chrome` `@finder` `@vscode`
- **Requêtes combinées** — tous les filtres sont combinables
- **Raccourci** — Cmd+Shift+C pour un accès rapide
- **Collage automatique** — Entrée colle directement dans l'application active
- **Quick Look** — Shift pour prévisualiser les images et fichiers

---

## Installation

### Installation directe (recommandée)

```bash
bash Makefile
```

Double-cliquez sur le fichier `build/Clipboard Search.alfredworkflow` généré.

### Installation développement

Lien symbolique dans le répertoire des workflows Alfred :

```bash
bash link.sh install    # Installer
bash link.sh uninstall  # Désinstaller
```

---

## Utilisation

### Principes de base

Tapez `cb` (configurable) dans Alfred, suivi de votre requête.

| Saisie | Résultat |
|---|---|
| `cb` | Afficher les entrées récentes (max 100) |
| `cb bonjour` | Recherche plein texte de "bonjour" |

### Filtres par type

```
cb :text         Texte uniquement
cb :image        Images uniquement
cb :file         Fichiers uniquement
```

`:txt` = `:text`, `:img` = `:image`.

### Filtres temporels

```
cb :today              Entrées du jour
cb :yesterday           Entrées d'hier
cb :2h                  Dernières 2 heures
cb :30m                 Dernières 30 minutes
cb :3d                  Derniers 3 jours
```

Unités : `h` (heures), `m` (minutes), `d` (jours).

### Filtres par date

```
cb :2026-05-10                    Date complète
cb :05-10                         Date courte (année courante)
cb :2026-05-01..2026-05-10       Plage de dates
cb :05-01..05-10                  Plage courte
```

### Filtres par application

```
cb @chrome          Depuis Chrome
cb @finder          Depuis le Finder
cb @vscode          Depuis VS Code
```

`@` prend en charge la correspondance floue (ex. `@chrome` correspond à "Google Chrome" et "Google Chrome Dev").

### Requêtes combinées

```
cb mot-clé :text :today @chrome
cb :image :today
cb :2026-05-01..2026-05-10 @vscode :text
```

---

## Opérations

| Touche | Action |
|---|---|
| **Entrée** | Collage automatique dans l'application active |
| **Shift** | Aperçu Quick Look |
| **Échap** | Fermer Alfred |

Chaque résultat affiche :
- **Titre** : première ligne / dimensions de l'image / nom du fichier
- **Sous-titre** : horodatage · application source · icône de type

---

## Configuration

Préférences Alfred → Workflows → Clipboard Search :

- **Mot-clé** : par défaut `cb`
- **Raccourci** : par défaut `Cmd+Shift+C`

---

## Fonctionnement

### Mécanisme de collage

```
Script Filter → Copy to Clipboard (autopaste=true, vitoclose=true)
```

Alfred ferme sa fenêtre → copie le texte dans le presse-papiers → exécute automatiquement Cmd+V. Toute la synchronisation est gérée en interne par Alfred, éliminant les problèmes de concurrence de focus.

### Base de données

Lit directement la base de données du presse-papiers d'Alfred :

```
~/Library/Application Support/Alfred/Databases/clipboard.alfdb
```

| Colonne | Description |
|---|---|
| `item` | Contenu texte / infos image / nom de fichier |
| `ts` | Temps absolu Mac (secondes depuis le 01/01/2001) |
| `app` | Nom de l'application source |
| `dataType` | 0=texte, 1=image, 2=fichier |
| `dataHash` | Hash pointant vers le fichier dans `clipboard.alfdb.data/` |

### Dépendances

Bibliothèque standard Python 3 uniquement — aucun paquet tiers requis.

---

## Structure

```
alfred/
├── README.md
├── Makefile
├── link.sh
├── .gitignore
└── src/clipboard-search/
    ├── info.plist
    ├── cb_search.py
    └── cb_paste.py
```

## Licence

MIT
