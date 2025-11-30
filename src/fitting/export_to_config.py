"""
export_to_config.py
-----------------------
This module saves fitted distribution results into a JSON configuration file.

The final structure looks like:

{
    "(1,2)_arr": { "dist": "weibull", "params": [shape, loc, scale] },
    "(3,3)_dep": { "dist": "gamma", "params": [shape, loc, scale] }
}

This file is called after:
- Fitting from CSV data
- Parsing EasyFit .edf files
- Or mixing both sources
"""

import json
import os


def export_distribution_config(result_dict, save_path):
    """
    Export fitted distribution configuration to JSON.

    Args:
        result_dict (dict):
            Keys are lane identifiers, e.g. "(1,2)_arr"
            Values are:
                {
                    "dist": "<distribution_name>",
                    "params": [param1, param2, param3]
                }

        save_path (str):
            File path where distributions.json will be stored.
    """

    # Make sure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Write JSON
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(result_dict, f, indent=4)

    print(f"[CONFIG] Exported {len(result_dict)} distributions → {save_path}")
