#!/usr/bin/env bash
# Symlink the workflow into Alfred's workflow directory for development.
# Usage: bash link.sh [install|uninstall]

set -euo pipefail

WORKFLOW_NAME="Clipboard Search"
WORKFLOW_DIR="$HOME/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src/clipboard-search"

# Generate a deterministic UUID for the workflow based on the bundle ID
WF_UUID="user.workflow.CB-SCRIPTFILTER"
TARGET="$WORKFLOW_DIR/$WF_UUID"

case "${1:-install}" in
    install)
        echo "Installing '$WORKFLOW_NAME' workflow..."
        if [ -L "$TARGET" ] || [ -d "$TARGET" ]; then
            echo "  Removing existing installation at $TARGET"
            rm -rf "$TARGET"
        fi
        ln -s "$SRC_DIR" "$TARGET"
        echo "  Symlinked: $SRC_DIR -> $TARGET"
        echo "Done. Restart Alfred or reload workflows to activate."
        ;;
    uninstall)
        echo "Uninstalling '$WORKFLOW_NAME' workflow..."
        if [ -L "$TARGET" ]; then
            rm "$TARGET"
            echo "  Removed symlink: $TARGET"
        elif [ -d "$TARGET" ]; then
            rm -rf "$TARGET"
            echo "  Removed directory: $TARGET"
        else
            echo "  Not installed."
        fi
        echo "Done."
        ;;
    *)
        echo "Usage: $0 [install|uninstall]"
        exit 1
        ;;
esac
