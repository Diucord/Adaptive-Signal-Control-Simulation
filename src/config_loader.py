"""
config_loader.py
-------------------------
Utility module for loading configuration JSON files.

All configuration files are stored under:

    src/config/

This loader provides a single function `load_json()` that:
- Builds the correct absolute path internally
- Opens the JSON file safely
- Returns the parsed dictionary
"""

import json
import os

# Determine the absolute path to the config directory
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")


def load_json(filename):
    """
    Load a JSON configuration file from the config directory.

    Args:
        filename (str):
            The JSON file name (e.g., "durations.json", "policies.json").

    Returns:
        dict: Parsed JSON contents.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If JSON is malformed.
    """
    path = os.path.join(CONFIG_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON file '{filename}': {e}")
