"""
Main entry point for the Adaptive Signal Control Simulation.

Supports:
- Fixed scheduling (--fixed)
- Adaptive scheduling (--adaptive)
- Full experiment mode (--experiment)
- Distribution fitting from datasets (--fit)
"""

import argparse
from src.config_loader import load_json
from src.config_validator import validate_all
from src.simulation_core import run_fixed, run_adaptive
from src.experiment import run_all_fixed_experiments
from src.adaptive_experiment import run_adaptive_experiment
from src.plotter import plot_results


def main():
    parser = argparse.ArgumentParser(description="Adaptive Signal Control Simulation")
    parser.add_argument("--fixed", action="store_true", help="Run fixed scheduling simulation")
    parser.add_argument("--adaptive", action="store_true", help="Run adaptive scheduling simulation")
    parser.add_argument("--experiment", action="store_true", help="Run all experiments (fixed+adaptive+plots)")
    parser.add_argument("--fit", action="store_true", help="Fit distributions from raw data")
    args = parser.parse_args()

    # Load configuration sets
    base        = load_json("base_settings.json")
    durations   = load_json("durations.json")["duration_sets"]
    policies    = load_json("policies.json")["policy_sets"]
    dists       = load_json("distributions.json")
    init        = load_json("init_conditions.json")
    capacity    = load_json("capacity.json")

    # Combine everything into one dictionary for validation
    configs = {
        "base": base,
        "durations": durations,
        "policies": policies,
        "dists": dists,
        "init": init,
        "caps": capacity
    }

    # Validate configurations
    validate_all(configs)

    # Run distribution fitting
    if args.fit:
        from src.fitting.fit_all_distributions import fit_all
        fit_all()
        return

    # Run simulations
    if args.fixed:
        print("Running FIXED simulation...")
        result = run_fixed(policies[0], durations[0], base["runtime"], base["seed"])
        print("Fixed result:", result)

    elif args.adaptive:
        print("Running ADAPTIVE simulation...")
        result = run_adaptive(policies[0], durations[0], base["runtime"], base["seed"])
        print("Adaptive result:", result)

    elif args.experiment:
        print("Running FULL experiment...")
        fixed_results = run_all_fixed_experiments()
        adaptive_results = run_adaptive_experiment()
        print("Fixed experiment results:", fixed_results)
        print("Adaptive experiment results:", adaptive_results)

        if base.get("save_plots", True):
            plot_results(fixed_results, adaptive_results)
            print("Plots saved under results/plots/")


if __name__ == "__main__":
    main()