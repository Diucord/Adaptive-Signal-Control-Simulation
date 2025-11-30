"""
fit_distributions.py
---------------------
Fit arrival/departure interval data to multiple distributions,
evaluate AIC/BIC, and choose the best model.

Supported models:
- GEV (Generalized Extreme Value)
- Lognormal
- Gamma
- Weibull
- Pareto
- Burr
- Logistic
- Rayleigh
- Normal
- Exponential

Returned format:
    ("distribution_name", [shape, loc, scale])
"""

import numpy as np
import scipy.stats as st


# Scipy distribution objects
MODEL_LIST = {
    "gev":          st.genextreme,
    "lognorm":      st.lognorm,
    "gamma":        st.gamma,
    "weibull":      st.weibull_min,
    "pareto":       st.pareto,
    "burr12":       st.burr12,
    "logistic":     st.logistic,
    "rayleigh":     st.rayleigh,
    "norm":         st.norm,
    "expon":        st.expon
}


def compute_aic(n_params, log_likelihood, n):
    """Compute AIC = 2k - 2ln(L)"""
    return 2 * n_params - 2 * log_likelihood


def compute_bic(n_params, log_likelihood, n):
    """Compute BIC = k ln(n) - 2ln(L)"""
    return n_params * np.log(n) - 2 * log_likelihood


def fit_model(dist, data):
    """
    Fit a SciPy distribution and compute ln-likelihood.
    Returns:
        (params, log_likelihood)
    """
    # Fit distribution parameters
    params = dist.fit(data)

    # Compute log-likelihood under fitted parameters
    log_pdf = dist.logpdf(data, *params)
    log_likelihood = np.sum(log_pdf)

    return params, log_likelihood


def auto_fit_distribution(data):
    """
    Try all supported models and select the best according to AIC.

    Args:
        data (array): cleaned arrival/departure interval samples.

    Returns:
        (best_name, best_params)
    """
    data = np.array(data)
    n = len(data)

    results = {}

    for name, dist in MODEL_LIST.items():
        try:
            params, ll = fit_model(dist, data)
            k = len(params)
            aic = compute_aic(k, ll, n)
            bic = compute_bic(k, ll, n)
            results[name] = (params, aic, bic)
        except Exception:
            continue  # Skip models that fail to converge

    # Choose best model based on minimum AIC
    best = min(results.items(), key=lambda x: x[1][1])  # compare AIC

    best_name = best[0]
    best_params = list(best[1][0])  # convert tuple → list

    return best_name, best_params
