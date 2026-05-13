[English](README.en.md) | [Español](README.es.md) | [日本語](README.ja.md) | [繁體中文](README.zh-Hant.md) | [简体中文](README.md)

# Recherche de presse-papiers · Clipboard Search for Alfred

![banner](https://raw.githubusercontent.com/kaikai-filu/clipboard-search-alfred-workflow/main/assets/banner-img.png)

Fonctionne avec l'historique du presse-papiers d'Alfred (fonctionnalité Powerpack).

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

Téléchargez le dernier `Clipboard Search.alfredworkflow` depuis [Releases](https://github.com/kaikai-filu/clipboard-search-alfred-workflow/releases) et double-cliquez pour installer.

### Compilation depuis les sources

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

Tous les filtres sont combinables :

```
cb mot-clé :text :today @chrome
cb :image :today
cb :2026-05-01..2026-05-10 @vscode :text
```

### Exemples concrets

```
cb :image :today                         Quelles captures d'écran ai-je prises aujourd'hui ?
cb curl :text :3d @iterm                Qu'ai-je curl récemment dans le terminal ?
cb TODO :text @vscode                   Quelles tâches restent dans mon code ?
cb :file @finder :yesterday             Fichiers copiés depuis le Finder hier ?
cb @chrome @safari :text :today         Texte copié depuis les navigateurs aujourd'hui ?
cb deploy :text :7d                      Tous les extraits liés à "deploy" cette semaine
cb error :30m @vscode                   Logs d'erreur de VS Code des 30 dernières minutes
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
- **Sous-titre** : horodatage · application source · icône de type · nombre de caractères · nombre de lignes (texte)

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
├── assets/
└── src/clipboard-search/
    ├── info.plist
    ├── cb_search.py
    └── cb_paste.py
```

---

## Développement assisté par IA

Développé avec Claude Code CLI (propulsé par DeepSeek-V4). Contributions clés :

- **Conception de l'architecture** — structure du workflow et connexions plist
- **Génération de code** — scripts Python, expressions régulières, AppleScript
- **Débogage** — analyse des logs Alfred pour identifier les problèmes de concurrence de focus
- **Documentation multilingue** — traductions en anglais, japonais, français, espagnol et chinois traditionnel

## Licence

MIT
