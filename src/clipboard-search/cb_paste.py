#!/usr/bin/env python3
"""Alfred Run Script action for pasting clipboard history items."""

import os
import sqlite3
import subprocess
import sys
from datetime import datetime

DB_PATH = os.path.expanduser(
    "~/Library/Application Support/Alfred/Databases/clipboard.alfdb"
)
DATA_DIR = DB_PATH + ".data"
DEBUG_LOG = "/tmp/cb_paste_debug.log"


def log(msg):
    try:
        with open(DEBUG_LOG, "a") as f:
            f.write(f"{datetime.now():%H:%M:%S.%f} {msg}\n")
    except Exception:
        pass


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


def paste():
    """Write a background AppleScript to a temp file and spawn it.

    The main script exits immediately so Alfred can close (vitoclose=true).
    The background osascript polls until Alfred loses focus, then pastes.
    """
    import tempfile

    script = """on run
    set logFile to "/tmp/cb_paste_debug.log"
    do shell script "date '+%H:%M:%S bg-start' >> " & quoted form of logFile

    repeat 30 times
        set frontApp to ""
        try
            tell application "System Events"
                set frontApp to name of first process whose frontmost is true
            end tell
        end try
        do shell script "echo 'bg-poll: " & frontApp & "' >> " & quoted form of logFile
        if frontApp is not "Alfred" and frontApp is not "Alfred 5" then exit repeat
        delay 0.1
    end repeat

    delay 0.3

    set frontApp to ""
    try
        tell application "System Events"
            set frontApp to name of first process whose frontmost is true
        end tell
    end try
    do shell script "echo 'bg-paste-into: " & frontApp & "' >> " & quoted form of logFile

    tell application "System Events"
        keystroke "v" using command down
    end tell

    do shell script "date '+%H:%M:%S bg-done' >> " & quoted form of logFile
end run"""

    fd, path = tempfile.mkstemp(suffix=".scpt", prefix="cb_paste_")
    with os.fdopen(fd, "w") as f:
        f.write(script)

    proc = subprocess.Popen(["osascript", path],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log(f"spawned bg paste pid={proc.pid} script={path}")


def main():
    log("=== cb_paste start ===")

    if len(sys.argv) < 2:
        log("ERROR: no argument")
        sys.exit(1)

    arg = sys.argv[1]
    copy_only = arg.startswith("copyonly:")
    ts = arg.replace("copyonly:", "", 1) if copy_only else arg
    log(f"arg={arg} ts={ts} copy_only={copy_only}")

    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT item, ts, app, dataType, dataHash FROM clipboard WHERE CAST(ts AS TEXT) = ?",
            (ts,),
        )
        row = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        log(f"DB error: {e}")
        sys.exit(1)

    if not row:
        log("No entry found")
        sys.exit(1)

    item = row["item"] or ""
    data_type = row["dataType"]
    data_hash = row["dataHash"] or ""
    log(f"data_type={data_type} item_preview={item[:60]}")

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
            log(f"Image file not found: {image_path}")
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
                    log(f"Original file not found: {original_path}")
                    sys.exit(1)
            else:
                log("Invalid plist format")
                sys.exit(1)
        else:
            alt_path = os.path.join(DATA_DIR, base_hash)
            if os.path.exists(alt_path):
                ok = set_clipboard_file(alt_path)
            else:
                log(f"No data found for hash: {base_hash}")
                sys.exit(1)
    else:
        log(f"Unknown data type: {data_type}")
        sys.exit(1)

    if not ok:
        log("Failed to copy to clipboard")
        sys.exit(1)

    log("copy OK")

    if copy_only:
        log("copy_only mode, skipping paste")
        return

    paste()
    log("=== cb_paste done ===")


if __name__ == "__main__":
    main()
