"""
plotter.py
----------------------
Generates visual comparison of:
- Fixed scheduling performance for all duration sets
- Adaptive scheduling performance

Saves PNG plots to results/plots/
"""

import os
import matplotlib.pyplot as plt
from .config_loader import load_json


def ensure_dir(path):
    """Create directory if not exists."""
    os.makedirs(path, exist_ok=True)


def plot_results(fixed_results, adaptive_results):
    """
    Plot comparison between:
    - mean delay of each fixed schedule
    - adaptive scheduling mean delay

    Args:
        fixed_results (list): from run_all_fixed_experiments()
        adaptive_results (dict): from run_adaptive_experiment()
    """
    cfg = load_json("base_settings.json")
    plot_dir = cfg["plot_dir"]
    ensure_dir(plot_dir)

    # Extract data
    fixed_means = [f["mean_delay"] for f in fixed_results]
    fixed_stds  = [f["std_delay"] for f in fixed_results]
    fixed_labels = [f"Set {i}" for i in range(len(fixed_results))]

    ada_mean = adaptive_results["mean_delay"]
    ada_std = adaptive_results["std_delay"]

    # Create plot
    plt.figure(figsize=(12, 6))
    plt.title("Comparison: Fixed Scheduling vs Adaptive Control")
    plt.xlabel("Experiment Set Index")
    plt.ylabel("Average Delay (sec)")

    # Fixed results
    plt.errorbar(
        list(range(len(fixed_means))),
        fixed_means,
        yerr=fixed_stds,
        fmt='o-', label="Fixed Scheduling"
    )

    # Adaptive result (horizontal line)
    plt.axhline(
        ada_mean,
        color='red',
        linestyle='--',
        label=f"Adaptive Mean (std={ada_std:.2f})"
    )

    plt.legend()
    plt.grid(True)
    save_path = os.path.join(plot_dir, "fixed_vs_adaptive.png")
    plt.savefig(save_path)
    plt.close()

    print(f"[PLOT] Saved plot → {save_path}")
