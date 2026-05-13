# Clipboard Search for Alfred

Works with Alfred Clipboard History (Powerpack feature).

Go beyond Alfred's built-in clipboard viewer — search and filter thousands of entries by keyword, type, time, date, and source application.

---

## Features

- **Keyword search** — full-text search across clipboard history
- **Type filters** — `:text` `:image` `:file`
- **Time filters** — `:today` `:yesterday` `:2h` `:30m` `:3d`
- **Date filters** — `:2026-05-10` `:05-10` (year optional) or ranges
- **App filters** — `@chrome` `@finder` `@vscode`
- **Combined queries** — all filters can be combined freely
- **Hotkey** — Cmd+Shift+C for quick access
- **Auto-paste** — Enter pastes directly into the frontmost application
- **Quick Look** — Shift to preview images and files

---

## Installation

### Direct Install (Recommended)

```bash
bash Makefile
```

Double-click the generated `build/Clipboard Search.alfredworkflow`.

### Development Install

Symlink into Alfred's workflow directory for instant reload during development:

```bash
bash link.sh install    # Install
bash link.sh uninstall  # Uninstall
```

---

## Usage

### Basics

Type `cb` (configurable) in Alfred, followed by your query.

| Input | Result |
|---|---|
| `cb` | Show recent entries (up to 100) |
| `cb hello` | Full-text search for "hello" |

### Type Filters

```
cb :text         Text entries only
cb :image        Image entries only
cb :file         File entries only
```

`:txt` = `:text`, `:img` = `:image`.

### Time Filters

```
cb :today              Today's entries
cb :yesterday           Yesterday's entries
cb :2h                  Last 2 hours
cb :30m                 Last 30 minutes
cb :3d                  Last 3 days
```

Units: `h` (hours), `m` (minutes), `d` (days).

### Date Filters

```
cb :2026-05-10                    Full date
cb :05-10                         Short date (current year assumed)
cb :2026-05-01..2026-05-10       Date range
cb :05-01..05-10                  Short date range
```

### App Filters

```
cb @chrome          From Chrome
cb @finder          From Finder
cb @vscode          From VS Code
```

`@` supports fuzzy matching (e.g. `@chrome` matches both "Google Chrome" and "Google Chrome Dev").

### Combined Queries

```
cb keyword :text :today @chrome
cb :image :today
cb :2026-05-01..2026-05-10 @vscode :text
```

### Real-world Examples

```
cb :image :today                         What screenshots did I take today?
cb curl :text :3d @iterm                What did I curl in the terminal recently?
cb TODO :text @vscode                   Which TODOs are left in my code?
cb :file @finder :yesterday             Files I copied from Finder yesterday?
cb @chrome @safari :text :today         What text did I copy from browsers today?
cb deploy :text :7d                      All "deploy"-related snippets this week
cb error :30m @vscode                   Error logs from VS Code in the last 30 min
```

---

## Operations

| Key | Action |
|---|---|
| **Enter** | Auto-paste into frontmost app |
| **Shift** | Quick Look preview |
| **Esc** | Close Alfred |

Each result displays:
- **Title**: first line / image dimensions / filename
- **Subtitle**: timestamp · source app · type icon · char count · line count (text entries)

---

## Configuration

Alfred Preferences → Workflows → Clipboard Search:

- **Keyword**: default `cb`
- **Hotkey**: default `Cmd+Shift+C`

---

## How It Works

### Paste Mechanism

```
Script Filter → Copy to Clipboard (autopaste=true, vitoclose=true)
```

Alfred closes its window → copies text to clipboard → auto-executes Cmd+V. All timing is handled internally by Alfred, eliminating focus race conditions.

### Database

Reads Alfred's own clipboard database directly:

```
~/Library/Application Support/Alfred/Databases/clipboard.alfdb
```

| Column | Description |
|---|---|
| `item` | Text content / image info / filename |
| `ts` | Mac absolute time (seconds since 2001-01-01) |
| `app` | Source application name |
| `dataType` | 0=text, 1=image, 2=file |
| `dataHash` | Hash pointing to file in `clipboard.alfdb.data/` |

### Dependencies

Python 3 standard library only — no third-party packages required.

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

## AI-Assisted Development

This project was developed with the help of Claude Code CLI, powered by DeepSeek-V4. Key contributions:

- **Architecture design** — workflow structure and plist connection wiring
- **Code generation** — Python scripts, regex patterns, AppleScript logic
- **Debugging** — analyzing Alfred Debug logs to identify focus race conditions
- **Multilingual docs** — English, Japanese, French, Spanish, and Traditional Chinese translations

> Claude Code is an AI coding assistant CLI that reads codebases, runs commands, and edits files — especially effective for multi-step workflows and cross-file refactors.

## License

MIT
