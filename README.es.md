[English](README.en.md) | [日本語](README.ja.md) | [Français](README.fr.md) | [繁體中文](README.zh-Hant.md) | [简体中文](README.md)

# Búsqueda de portapapeles · Clipboard Search for Alfred

![banner](https://raw.githubusercontent.com/kaikai-filu/clipboard-search-alfred-workflow/main/assets/banner-img.png)

Funciona con el historial del portapapeles de Alfred (funcionalidad Powerpack).

Supera el visor de portapapeles integrado de Alfred — busca y filtra miles de entradas por palabra clave, tipo, hora, fecha y aplicación de origen.

---

## Funcionalidades

- **Búsqueda por palabra clave** — búsqueda de texto completo en el historial
- **Filtros por tipo** — `:text` `:image` `:file`
- **Filtros temporales** — `:today` `:yesterday` `:2h` `:30m` `:3d`
- **Filtros por fecha** — `:2026-05-10` `:05-10` (año opcional) o rangos
- **Filtros por aplicación** — `@chrome` `@finder` `@vscode`
- **Consultas combinadas** — todos los filtros se pueden combinar libremente
- **Atajo de teclado** — Cmd+Shift+C para acceso rápido
- **Auto-pegar** — Enter pega directamente en la aplicación activa
- **Quick Look** — Shift para previsualizar imágenes y archivos

---

## Instalación

### Instalación directa (recomendada)

Descarga el último `Clipboard Search.alfredworkflow` desde [Releases](https://github.com/kaikai-filu/clipboard-search-alfred-workflow/releases) y haz doble clic para instalar.

### Compilar desde el código fuente

```bash
bash Makefile
```

Haz doble clic en el archivo generado `build/Clipboard Search.alfredworkflow`.

### Instalación para desarrollo

Enlace simbólico al directorio de workflows de Alfred:

```bash
bash link.sh install    # Instalar
bash link.sh uninstall  # Desinstalar
```

---

## Uso

### Conceptos básicos

Escribe `cb` (configurable) en Alfred, seguido de tu consulta.

| Entrada | Resultado |
|---|---|
| `cb` | Mostrar entradas recientes (máx. 100) |
| `cb hola` | Búsqueda de texto completo de "hola" |

### Filtros por tipo

```
cb :text         Solo texto
cb :image        Solo imágenes
cb :file         Solo archivos
```

`:txt` = `:text`, `:img` = `:image`.

### Filtros temporales

```
cb :today              Entradas de hoy
cb :yesterday           Entradas de ayer
cb :2h                  Últimas 2 horas
cb :30m                 Últimos 30 minutos
cb :3d                  Últimos 3 días
```

Unidades: `h` (horas), `m` (minutos), `d` (días).

### Filtros por fecha

```
cb :2026-05-10                    Fecha completa
cb :05-10                         Fecha corta (año actual)
cb :2026-05-01..2026-05-10       Rango de fechas
cb :05-01..05-10                  Rango corto
```

### Filtros por aplicación

```
cb @chrome          Desde Chrome
cb @finder          Desde Finder
cb @vscode          Desde VS Code
```

`@` admite coincidencia difusa (ej. `@chrome` coincide con "Google Chrome" y "Google Chrome Dev").

### Consultas combinadas

Todos los filtros se pueden combinar:

```
cb palabra :text :today @chrome
cb :image :today
cb :2026-05-01..2026-05-10 @vscode :text
```

### Ejemplos prácticos

```
cb :image :today                         ¿Qué capturas de pantalla tomé hoy?
cb curl :text :3d @iterm                ¿Qué curl hice en la terminal recientemente?
cb TODO :text @vscode                   ¿Qué tareas pendientes hay en mi código?
cb :file @finder :yesterday             ¿Archivos copiados del Finder ayer?
cb @chrome @safari :text :today         ¿Texto copiado de navegadores hoy?
cb deploy :text :7d                      Todos los fragmentos sobre "deploy" esta semana
cb error :30m @vscode                   Logs de error de VS Code en los últimos 30 min
```

---

## Operaciones

| Tecla | Acción |
|---|---|
| **Enter** | Auto-pegar en la aplicación activa |
| **Shift** | Vista previa Quick Look |
| **Esc** | Cerrar Alfred |

Cada resultado muestra:
- **Título**: primera línea / dimensiones de imagen / nombre de archivo
- **Subtítulo**: marca de tiempo · aplicación de origen · icono de tipo · caracteres · líneas (texto)

---

## Configuración

Preferencias de Alfred → Workflows → Clipboard Search:

- **Palabra clave**: por defecto `cb`
- **Atajo**: por defecto `Cmd+Shift+C`

---

## Funcionamiento

### Mecanismo de pegado

```
Script Filter → Copy to Clipboard (autopaste=true, vitoclose=true)
```

Alfred cierra su ventana → copia el texto al portapapeles → ejecuta automáticamente Cmd+V. Toda la sincronización es gestionada internamente por Alfred, eliminando los problemas de competencia de foco.

### Base de datos

Lee directamente la base de datos del portapapeles de Alfred:

```
~/Library/Application Support/Alfred/Databases/clipboard.alfdb
```

| Columna | Descripción |
|---|---|
| `item` | Contenido de texto / info de imagen / nombre de archivo |
| `ts` | Tiempo absoluto Mac (segundos desde 2001-01-01) |
| `app` | Nombre de la aplicación de origen |
| `dataType` | 0=texto, 1=imagen, 2=archivo |
| `dataHash` | Hash que apunta al archivo en `clipboard.alfdb.data/` |

### Dependencias

Solo biblioteca estándar de Python 3 — no se requieren paquetes de terceros.

---

## Estructura

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

## Desarrollo asistido por IA

Desarrollado con Claude Code CLI (impulsado por DeepSeek-V4). Contribuciones clave:

- **Diseño de arquitectura** — estructura del workflow y conexiones plist
- **Generación de código** — scripts Python, expresiones regulares, AppleScript
- **Depuración** — análisis de logs de Alfred para identificar problemas de concurrencia de foco
- **Documentación multilingüe** — traducciones al inglés, japonés, francés, español y chino tradicional

## Licencia

MIT
