"""
fit_all_distributions.py
-------------------------
Full automated workflow for:

1. Loading raw interval data (CSV)
2. OR loading EasyFit `.edf` exported results
3. Fitting distributions (AIC/BIC-based selection)
4. Exporting final parameters to `config/distributions.json`
"""

import os
import json
import glob
import numpy as np
from .dataset_loader import load_dataset
from .parse_edf import parse_edf
from .fit_distributions import auto_fit_distribution
from .export_to_config import export_distribution_config


def fit_all(data_dir="data/", save_path="src/config/distributions.json"):
    """
    Automatically fit all arrival/departure distributions.

    Expected directory structure:

        data/
            arr_12.csv
            dep_12.csv
            arr_33.edf
            dep_41.edf
            ...

    The function automatically detects:
    - CSV files (raw intervals)
    - EDF files (EasyFit export)

    Args:
        data_dir (str): folder containing input datasets.
        save_path (str): where to save the output distributions.json
    """

    files = glob.glob(os.path.join(data_dir, "*"))

    results = {}

    for file in files:
        fname = os.path.basename(file).lower()

        # Lane index extraction
        # Example: arr_12.csv → (1,2)
        lane_match = __import__("re").search(r"(arr|dep)_([1-4])([1-3])", fname)
        if not lane_match:
            continue

        kind = lane_match.group(1)   # arr or dep
        i = lane_match.group(2)
        j = lane_match.group(3)

        key = f"({i},{j})_{kind}"

        # CASE 1: CSV raw data (direct intervals)
        if fname.endswith(".csv"):
            df = load_dataset(file)
            column = "arr_time" if kind == "arr" else "dep_time"
            data = df[column].dropna().values
            dist_name, params = auto_fit_distribution(data)
            results[key] = {"dist": dist_name, "params": params}
            print(f"[FIT] {file} -> {dist_name} {params}")

        # CASE 2: EasyFit EDF file → parse + convert to JSON
        elif fname.endswith(".edf"):
            d = parse_edf(file)
            results[key] = d
            print(f"[EDF] Loaded EasyFit model for {file}")

    # Export everything to JSON
    export_distribution_config(results, save_path)
    print(f"\nSaved final distributions to {save_path}")
