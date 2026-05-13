#!/usr/bin/env python3
"""Alfred Script Filter for searching clipboard history.

Queries Alfred's clipboard database with support for:
- Keyword search (full-text)
- Type filters (:text, :image, :file)
- Time filters (:today, :yesterday, :N[hmd])
- App filters (@appname)
"""

import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

DB_PATH = os.path.expanduser(
    "~/Library/Application Support/Alfred/Databases/clipboard.alfdb"
)
DATA_DIR = DB_PATH + ".data"

# Mac absolute time: seconds since 2001-01-01 00:00:00 UTC
MAC_EPOCH_DELTA = 978307200

MAX_RESULTS = 100

TYPE_NAMES = {0: "text", 1: "image", 2: "file"}
TYPE_EMOJI = {0: "\U0001f4dd", 1: "\U0001f5bc", 2: "\U0001f4c1"}


def mac_ts_to_datetime(mac_ts):
    unix_ts = mac_ts + MAC_EPOCH_DELTA
    return datetime.fromtimestamp(unix_ts, tz=timezone.utc)


def parse_query(query_str):
    if not query_str:
        return {"keyword": "", "types": set(), "time_start": None, "time_end": None, "app": None}

    types = set()
    time_start = None
    time_end = None
    app = None
    keyword_parts = []

    now = datetime.now().astimezone()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    for token in query_str.split():
        if token in (":text", ":txt"):
            types.add(0)
        elif token in (":image", ":img"):
            types.add(1)
        elif token in (":file", ":files"):
            types.add(2)
        elif token == ":today":
            time_start = today_start
            time_end = now
        elif token == ":yesterday":
            time_start = today_start - timedelta(days=1)
            time_end = today_start
        elif m := re.match(r"^:(\d+)([hmd])$", token):
            num = int(m.group(1))
            unit = m.group(2)
            delta = {"h": timedelta(hours=num), "m": timedelta(minutes=num), "d": timedelta(days=num)}[unit]
            time_start = now - delta
            time_end = now
        elif m := re.match(r"^:(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})$", token):
            try:
                time_start = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=now.tzinfo)
                time_end = (datetime.strptime(m.group(2), "%Y-%m-%d") + timedelta(days=1)).replace(tzinfo=now.tzinfo)
            except ValueError:
                keyword_parts.append(token)
        elif m := re.match(r"^:(\d{2}-\d{2})\.\.(\d{2}-\d{2})$", token):
            try:
                y = str(now.year)
                time_start = datetime.strptime(f"{y}-{m.group(1)}", "%Y-%m-%d").replace(tzinfo=now.tzinfo)
                time_end = (datetime.strptime(f"{y}-{m.group(2)}", "%Y-%m-%d") + timedelta(days=1)).replace(tzinfo=now.tzinfo)
            except ValueError:
                keyword_parts.append(token)
        elif m := re.match(r"^:(\d{4}-\d{2}-\d{2})$", token):
            try:
                d = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=now.tzinfo)
                time_start = d
                time_end = d + timedelta(days=1)
            except ValueError:
                keyword_parts.append(token)
        elif m := re.match(r"^:(\d{2}-\d{2})$", token):
            try:
                d = datetime.strptime(f"{now.year}-{m.group(1)}", "%Y-%m-%d").replace(tzinfo=now.tzinfo)
                time_start = d
                time_end = d + timedelta(days=1)
            except ValueError:
                keyword_parts.append(token)
        elif token.startswith("@"):
            app = token[1:]
        else:
            keyword_parts.append(token)

    return {
        "keyword": " ".join(keyword_parts),
        "types": types,
        "time_start": time_start,
        "time_end": time_end,
        "app": app,
    }


def build_query(filters):
    conditions = []
    params = []

    if filters["keyword"]:
        conditions.append("item LIKE ?")
        params.append(f"%{filters['keyword']}%")
    if filters["types"]:
        placeholders = ",".join("?" * len(filters["types"]))
        conditions.append(f"dataType IN ({placeholders})")
        params.extend(sorted(filters["types"]))
    if filters["time_start"]:
        conditions.append("ts >= ?")
        params.append(filters["time_start"].timestamp() - MAC_EPOCH_DELTA)
    if filters["time_end"]:
        conditions.append("ts < ?")
        params.append(filters["time_end"].timestamp() - MAC_EPOCH_DELTA)
    if filters["app"]:
        conditions.append("app LIKE ?")
        params.append(f"%{filters['app']}%")

    where = " AND ".join(conditions) if conditions else "1=1"
    return (
        f"SELECT item, ts, app, apppath, dataType, dataHash FROM clipboard "
        f"WHERE {where} ORDER BY ts DESC LIMIT {MAX_RESULTS}",
        params,
    )


def build_quicklook_url(data_type, data_hash):
    """Build a file:// URL for Quick Look preview of images and files."""
    if not data_hash:
        return None

    if data_type == 1:
        path = os.path.join(DATA_DIR, data_hash.replace(".tiff", "") + ".tiff")
        if os.path.exists(path):
            return "file://" + path
    elif data_type == 2:
        plist_path = os.path.join(DATA_DIR, data_hash)
        if os.path.exists(plist_path):
            import plistlib
            try:
                with open(plist_path, "rb") as f:
                    plist_data = plistlib.load(f)
                if isinstance(plist_data, list) and plist_data:
                    original_path = plist_data[0]
                    if os.path.exists(original_path):
                        return "file://" + original_path
            except Exception:
                pass
    return None


def format_item(row):
    item = row["item"] or ""
    ts = row["ts"]
    app = row["app"] or "Unknown"
    data_type = row["dataType"]
    data_hash = row["dataHash"] or ""

    dt = mac_ts_to_datetime(ts).astimezone()
    dt_str = dt.strftime("%Y-%m-%d %H:%M")
    emoji = TYPE_EMOJI.get(data_type, "\U0001f4cb")
    type_name = TYPE_NAMES.get(data_type, "unknown")

    if data_type == 0:
        text = item
        lines = text.split("\n")
        first_line = lines[0].strip()
        title = first_line[:100] if first_line else "(empty)"
        chars = len(text)
        line_count = len(lines)
        subtitle = f"{dt_str}  {app}  {emoji} {type_name}  {chars} chars · {line_count} lines"
        # Pass the actual text content as arg so Copy to Clipboard can auto-paste it
        arg = item
    elif data_type == 1:
        title = item or "Image"
        subtitle = f"{dt_str}  {app}  {emoji} {type_name}"
        arg = f"paste:{ts}"
    elif data_type == 2:
        filename = item.replace("File: ", "") if item.startswith("File: ") else (item or "File")
        title = filename
        subtitle = f"{dt_str}  {app}  {emoji} {type_name}"
        arg = f"paste:{ts}"
    else:
        title = str(item)[:100] if item else "(unknown)"
        subtitle = f"{dt_str}  {app}  {emoji} {type_name}"
        arg = f"paste:{ts}"

    apppath = row["apppath"] or ""
    icon = None
    if apppath and os.path.exists(apppath):
        icon = {"path": apppath, "type": "fileicon"}

    result = {
        "uid": str(ts),
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "text": {
            "copy": item if data_type == 0 else title,
            "largetype": item if data_type == 0 else title,
        },
        "mods": {
            "cmd": {
                "arg": "copyonly:" + str(ts),
                "subtitle": f"仅复制到剪贴板  {title}",
            }
        },
    }
    if icon:
        result["icon"] = icon

    ql = build_quicklook_url(data_type, data_hash)
    if ql:
        result["quicklookurl"] = ql

    return result


def main():
    query_str = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    filters = parse_query(query_str)
    sql, params = build_query(filters)

    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(json.dumps({
            "items": [{"title": "Database Error", "subtitle": str(e), "valid": False}]
        }))
        return

    if not rows:
        subtitle = f"Query: {query_str}" if query_str else "no recent entries"
        print(json.dumps({
            "items": [{"title": "\U0001f50d No clipboard entries found", "subtitle": subtitle, "valid": False}]
        }))
        return

    items = [format_item(row) for row in rows]
    print(json.dumps({"items": items}))


if __name__ == "__main__":
    main()
