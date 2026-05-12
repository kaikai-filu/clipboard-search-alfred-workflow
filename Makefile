#!/usr/bin/env bash
# Build the .alfredworkflow package for distribution.
# Usage: bash Makefile

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src/clipboard-search"
BUILD_DIR="$SCRIPT_DIR/build"
OUTPUT="$BUILD_DIR/Clipboard Search.alfredworkflow"

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Copy workflow files
cp -r "$SRC_DIR" "$BUILD_DIR/workflow"

# Remove any __pycache__
find "$BUILD_DIR/workflow" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Create .alfredworkflow (zip with the workflow directory contents)
cd "$BUILD_DIR/workflow"
zip -r "$OUTPUT" . -x "*.DS_Store"
cd "$SCRIPT_DIR"

echo "Built: $OUTPUT"
ls -lh "$OUTPUT"
