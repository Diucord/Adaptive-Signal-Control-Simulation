"""
experiment.py
------------------------
Provides experiment manager for fixed-schedule simulations.

Features:
- Run multiple duration sets (grid search)
- Repeat each run N times
- Compute mean and standard deviation
- Return full result table
"""

import numpy as np
from .simulation_core import run_fixed
from .config_loader import load_json


def run_all_fixed_experiments():
    """
    Run fixed-duration experiments over all duration sets.

    Returns:
        results (list):
            [
                {
                    "duration_set": [...],
                    "mean_delay": float,
                    "std_delay": float
                },
                ...
            ]
    """
    durations_all = load_json("durations.json")["duration_sets"]
    policies = load_json("policies.json")["policy_sets"]
    base = load_json("base_settings.json")

    fixed_rep = base["fixed_rep"]
    runtime = base["runtime"]
    seed = base["seed"]

    results = []

    for idx, duration_set in enumerate(durations_all):
        print(f"[FIXED-EXPERIMENT] Set {idx}: duration={duration_set}")

        policy = policies[idx] if idx < len(policies) else policies[0]

        samples = []
        for r in range(fixed_rep):
            s = seed + idx * 100 + r
            avg_delay = run_fixed(policy, duration_set, runtime, s)
            samples.append(avg_delay)
            print(f"  Run {r+1}/{fixed_rep} → delay={avg_delay:.4f}")

        results.append({
            "duration_set": duration_set,
            "mean_delay": float(np.mean(samples)),
            "std_delay": float(np.std(samples))
        })

    print("\n[FIXED-EXPERIMENT] Completed.")
    return results
