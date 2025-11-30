"""
distributions_dynamic.py
--------------------------------
Provides a universal interface for loading and evaluating
inverse CDF (PPF) for any distribution declared in `distributions.json`.

Supports:
- Any SciPy-supported distribution
- EasyFit-exported distribution names
- Automatic name normalization (lowercase, no spaces)
- Arbitrary number of parameters (shape, loc, scale,…)

This module is the core of the dynamic distribution system:
Simulation never needs to know which distribution is used.
"""

import numpy as np
import scipy.stats as st


# ---------------------------------------------------------
# Distribution registry
# Add more entries here if needed.
# Keys should be normalized lowercase names.
# ---------------------------------------------------------

DISTRIBUTION_MAP = {
    # Core distributions
    "gev": st.genextreme,
    "generalizedextremevalue": st.genextreme,

    "lognorm": st.lognorm,
    "lognormal": st.lognorm,

    "gamma": st.gamma,
    "weibull": st.weibull_min,
    "weibullmin": st.weibull_min,

    "pareto": st.pareto,
    "burr": st.burr,
    "burr12": st.burr12,

    "beta": st.beta,
    "chi2": st.chi2,
    "chisquare": st.chi2,

    "logistic": st.logistic,
    "rayleigh": st.rayleigh,
    "uniform": st.uniform,

    # Standard distributions
    "norm": st.norm,
    "normal": st.norm,
    "gaussian": st.norm,

    "expon": st.expon,
    "exponential": st.expon,
}


# ---------------------------------------------------------
# Helper: Normalize distribution names
# ---------------------------------------------------------

def _normalize_name(name: str) -> str:
    """
    Normalize distribution name:
    - lowercase
    - remove spaces
    - strip special characters

    Args:
        name (str)

    Returns:
        normalized name (str)
    """
    return name.lower().replace(" ", "").strip()


# ---------------------------------------------------------
# Inverse CDF (PPF) wrapper
# ---------------------------------------------------------

def get_inverse_cdf(dist_name, params, p):
    """
    Compute inverse CDF (PPF) for any configured distribution.

    Args:
        dist_name (str):
            Distribution name from EasyFit or SciPy.
        params (list):
            Distribution parameters exactly as specified in JSON.
            Typically shape, loc, scale — but supports any size.
        p (float):
            Random probability (0–1).

    Returns:
        float: inverse CDF value
    """
    name = _normalize_name(dist_name)

    if name not in DISTRIBUTION_MAP:
        raise ValueError(
            f"Unsupported distribution '{dist_name}'. "
            f"Normalized key '{name}' not found in DISTRIBUTION_MAP."
        )

    dist = DISTRIBUTION_MAP[name]

    # SciPy distribution objects accept parameters as *args
    try:
        return float(dist(*params).ppf(p))
    except Exception as e:
        raise RuntimeError(
            f"Failed computing PPF for '{dist_name}' "
            f"with params={params}, p={p}: {e}"
        )
