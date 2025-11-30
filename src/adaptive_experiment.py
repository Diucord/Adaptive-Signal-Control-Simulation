"""
adaptive_experiment.py
-------------------------------
Runs adaptive scheduling experiment:
- Repeats adaptive control simulation N times
- Computes mean delay and std deviation
- Returns results for comparison with fixed experiments
"""

import numpy as np
from .simulation_core import run_adaptive
from .config_loader import load_json


def run_adaptive_experiment():
    """
    Run repeated adaptive scheduling experiments.

    Returns:
        dict {
            "mean_delay": float,
            "std_delay": float,
            "samples": [...]
        }
    """
    base = load_json("base_settings.json")
    durations = load_json("durations.json")["duration_sets"]
    policies  = load_json("policies.json")["policy_sets"]

    adaptive_rep = base["adaptive_rep"]
    runtime = base["runtime"]
    seed = base["seed"]

    # Use first policy/duration as base
    policy = policies[0]
    duration_set = durations[0]

    samples = []

    print(f"[ADAPTIVE-EXPERIMENT] Running {adaptive_rep} trials...")

    for r in range(adaptive_rep):
        s = seed + 999 + r
        avg_delay = run_adaptive(policy, duration_set, runtime, s)
        samples.append(avg_delay)
        print(f"  Run {r+1}/{adaptive_rep} → delay={avg_delay:.4f}")

    results = {
        "mean_delay": float(np.mean(samples)),
        "std_delay": float(np.std(samples)),
        "samples": samples
    }

    print("[ADAPTIVE-EXPERIMENT] Completed.")
    return results
