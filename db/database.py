"""
db/database.py
--------------
JSON-based Storage Layer.

Design principle: all file I/O is encapsulated here.
No other module should open/read/write storage.json directly.
This makes it trivial to swap JSON for PostgreSQL, SQLite, or Redis
later — just replace this file's internals; the interface stays the same.

Public interface:
    save_data(record: dict) -> None
    load_data()             -> list
    clear_data()            -> None
"""

import json
import os
from typing import Any

from config.settings import STORAGE_FILE
from utils.logger import log


def _ensure_file_exists() -> None:
    """
    Create the storage file and its parent directory if they don't exist.
    Called internally before any read/write operation.
    """
    os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)
    if not os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "w") as f:
            json.dump([], f)


def load_data() -> list:
    """
    Load all records from the JSON storage file.

    Returns:
        A list of dicts representing stored records.
        Returns an empty list if the file is missing or corrupted.
    """
    _ensure_file_exists()
    try:
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                log("warning", "Database", "Storage file root is not a list. Resetting.")
                return []
            return data
    except json.JSONDecodeError as e:
        log("error", "Database", f"JSON decode error: {e}. Returning empty dataset.")
        return []
    except IOError as e:
        log("error", "Database", f"File read error: {e}")
        return []


def save_data(record: dict) -> None:
    """
    Append a new record to the JSON storage file.

    Args:
        record: Any dict to persist. Expected to contain at minimum
                'asset', 'price', and 'timestamp' keys.
    """
    if not isinstance(record, dict):
        log("warning", "Database", f"save_data received non-dict: {type(record)}. Skipping.")
        return

    records = load_data()
    records.append(record)

    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(records, f, indent=2)
        log("debug", "Database", f"Saved record. Total stored: {len(records)}")
    except IOError as e:
        log("error", "Database", f"File write error: {e}")


def clear_data() -> None:
    """
    Wipe all records from storage. Resets the file to an empty list.
    Use with care — intended for testing and resets only.
    """
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump([], f)
        log("info", "Database", "Storage cleared.")
    except IOError as e:
        log("error", "Database", f"Could not clear storage: {e}")
