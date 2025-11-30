"""
parse_edf.py
-------------------
This module parses EasyFit `.edf` exported files.

EasyFit stores fitted results in a human-readable text format like:

    Distribution: Weibull
    Parameters:
        Shape = 2.14
        Scale = 1.83
        Location = 0.00

This parser extracts:
- distribution name (e.g., "Weibull")
- parameters in SciPy-friendly order (shape, loc, scale)

Returned Format:
    {
        "dist": "Weibull",
        "params": [shape, loc, scale]
    }
"""

import re


def parse_edf(path):
    """
    Parse an EasyFit .edf file and return distribution info.

    Args:
        path (str): File path to the .edf file.

    Returns:
        dict: {
            "dist": <distribution_name>,
            "params": [param1, param2, param3]
        }
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Extract distribution name
    dist_match = re.search(r"Distribution:\s*([A-Za-z0-9_\- ]+)", text)
    if not dist_match:
        raise ValueError(f"Cannot find distribution name in {path}")

    dist_name = dist_match.group(1).strip()

    # Extract parameters (shape, scale, location, etc.)
    param_matches = re.findall(r"([A-Za-z]+)\s*=\s*([-0-9\.]+)", text)

    # Convert to SciPy's parameter order:
    # Many SciPy distributions use (shape, loc, scale)
    # If EasyFit doesn't provide all, missing values default to 0 or 1 depending on distribution.

    params_dict = {k.lower(): float(v) for k, v in param_matches}

    # Build params list following SciPy's "shape, loc, scale" convention:
    shape = params_dict.get("shape", None)
    loc   = params_dict.get("location", 0.0)
    scale = params_dict.get("scale", params_dict.get("rate", 1.0))

    # Pack into final format
    params = []

    if shape is not None:
        params.append(shape)

    # Most SciPy distributions use at least (loc, scale)
    params.append(loc)
    params.append(scale)

    return {
        "dist": dist_name,
        "params": params
    }
