#!/usr/bin/env python3
"""Alfred Run Script action for Cmd+Enter: copy clipboard item to system clipboard.

Only used for the Cmd+Enter modifier path. The Enter path uses Alfred's
built-in Copy to Clipboard output with auto-paste.
"""

import os
import sqlite3
import subprocess
import sys

DB_PATH = os.path.expanduser(
    "~/Library/Application Support/Alfred/Databases/clipboard.alfdb"
)
DATA_DIR = DB_PATH + ".data"


def set_clipboard_text(text):
    proc = subprocess.run(["pbcopy"], input=text, text=True, timeout=5)
    return proc.returncode == 0


def set_clipboard_file(filepath):
    applescript = (
        'set the clipboard to (POSIX file "{path}" as alias)'.format(path=filepath)
    )
    proc = subprocess.run(
        ["osascript", "-e", applescript], capture_output=True, text=True, timeout=10
    )
    return proc.returncode == 0


def set_clipboard_image(image_path):
    applescript = '''
    use framework "AppKit"
    use scripting additions
    set img to current application's NSImage's alloc()'s initWithContentsOfFile:"{path}"
    if img is missing value then
        error "Failed to load image"
    end if
    set pb to current application's NSPasteboard's generalPasteboard()
    pb's clearContents()
    pb's writeObject:img
    '''.format(path=image_path)
    proc = subprocess.run(
        ["osascript", "-e", applescript], capture_output=True, text=True, timeout=10
    )
    return proc.returncode == 0


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    arg = sys.argv[1]
    ts = arg.replace("copyonly:", "", 1) if arg.startswith("copyonly:") else arg

    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT item, dataType, dataHash FROM clipboard WHERE CAST(ts AS TEXT) = ?",
            (ts,),
        )
        row = cursor.fetchone()
        conn.close()
    except sqlite3.Error:
        sys.exit(1)

    if not row:
        sys.exit(1)

    item = row["item"] or ""
    data_type = row["dataType"]
    data_hash = row["dataHash"] or ""

    if data_type == 0:
        set_clipboard_text(item)
    elif data_type == 1:
        base_hash = data_hash.replace(".tiff", "")
        image_path = os.path.join(DATA_DIR, base_hash + ".tiff")
        if os.path.exists(image_path):
            if not set_clipboard_image(image_path):
                set_clipboard_file(image_path)
    elif data_type == 2:
        base_hash = data_hash.replace(".tiff", "")
        plist_path = os.path.join(DATA_DIR, base_hash + ".plist")
        if os.path.exists(plist_path):
            import plistlib
            with open(plist_path, "rb") as f:
                plist_data = plistlib.load(f)
            if isinstance(plist_data, list) and plist_data:
                original_path = plist_data[0]
                if os.path.exists(original_path):
                    set_clipboard_file(original_path)


if __name__ == "__main__":
    main()
