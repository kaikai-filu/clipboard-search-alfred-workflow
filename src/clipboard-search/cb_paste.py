#!/usr/bin/env python3
"""Alfred Run Script action for pasting clipboard history items.

Receives the ts value (Mac absolute time) as argument, fetches the
corresponding clipboard entry from the database, copies it to the
system clipboard, and then simulates Cmd+V to paste into the
previously focused application.
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
    """Copy plain text to the system clipboard."""
    proc = subprocess.run(["pbcopy"], input=text, text=True, timeout=5)
    return proc.returncode == 0


def set_clipboard_file(filepath):
    """Copy a file reference to the Finder clipboard via osascript."""
    applescript = (
        'set the clipboard to (POSIX file "{path}" as alias)'.format(
            path=filepath
        )
    )
    proc = subprocess.run(
        ["osascript", "-e", applescript], capture_output=True, text=True, timeout=10
    )
    return proc.returncode == 0


def set_clipboard_image(image_path):
    """Copy an image to the clipboard as an image via osascript."""
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


def paste():
    """Hide Alfred, wait for previous app to regain focus, then Cmd+V."""
    applescript = '''
    tell application "System Events"
        -- Hide Alfred
        if exists process "Alfred" then
            set visible of process "Alfred" to false
        end if

        -- Wait until Alfred is no longer frontmost (max 2 seconds)
        repeat 20 times
            set frontApp to name of first process whose frontmost is true
            if frontApp is not "Alfred" and frontApp is not "Alfred 5" then
                exit repeat
            end if
            delay 0.1
        end repeat

        -- Paste into the now-frontmost app
        keystroke "v" using command down
    end tell
    '''
    subprocess.run(
        ["osascript", "-e", applescript],
        capture_output=True, text=True, timeout=5,
    )


def main():
    if len(sys.argv) < 2:
        print("No argument provided", file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]
    copy_only = arg.startswith("copyonly:")
    ts = arg.replace("copyonly:", "", 1) if copy_only else arg

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT item, ts, app, dataType, dataHash FROM clipboard WHERE CAST(ts AS TEXT) = ?",
            (ts,),
        )
        row = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1)

    if not row:
        print(f"No entry found for ts={ts}", file=sys.stderr)
        sys.exit(1)

    item = row["item"] or ""
    data_type = row["dataType"]
    data_hash = row["dataHash"] or ""

    ok = False

    if data_type == 0:
        ok = set_clipboard_text(item)
    elif data_type == 1:
        base_hash = data_hash.replace(".tiff", "")
        image_path = os.path.join(DATA_DIR, base_hash + ".tiff")
        if os.path.exists(image_path):
            ok = set_clipboard_image(image_path)
            if not ok:
                ok = set_clipboard_file(image_path)
        else:
            print(f"Image file not found: {image_path}", file=sys.stderr)
            sys.exit(1)
    elif data_type == 2:
        base_hash = data_hash.replace(".tiff", "")
        plist_path = os.path.join(DATA_DIR, base_hash + ".plist")
        if os.path.exists(plist_path):
            import plistlib
            with open(plist_path, "rb") as f:
                plist_data = plistlib.load(f)
            if isinstance(plist_data, list) and len(plist_data) > 0:
                original_path = plist_data[0]
                if os.path.exists(original_path):
                    ok = set_clipboard_file(original_path)
                else:
                    print(f"Original file not found: {original_path}", file=sys.stderr)
                    sys.exit(1)
            else:
                print("Invalid plist format", file=sys.stderr)
                sys.exit(1)
        else:
            alt_path = os.path.join(DATA_DIR, base_hash)
            if os.path.exists(alt_path):
                ok = set_clipboard_file(alt_path)
            else:
                print(f"No data found for hash: {base_hash}", file=sys.stderr)
                sys.exit(1)
    else:
        print(f"Unknown data type: {data_type}", file=sys.stderr)
        sys.exit(1)

    if not ok:
        print("Failed to copy to clipboard", file=sys.stderr)
        sys.exit(1)

    if copy_only:
        return

    # Auto-paste into the frontmost app
    paste()


if __name__ == "__main__":
    main()
