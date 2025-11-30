# Adaptive Signal Control Simulation  
Traffic Intersection Simulation with Dynamic Distribution Fitting, Adaptive Signal Timing, and Modular Configuration

---

## Overview
This project implements a **modular, fully-configurable traffic signal simulation**, supporting:

- **Fixed-time signal control**
- **Adaptive signal timing (pressure-based)**
- **Dynamic arrival/departure distribution fitting**
- **EasyFit (.edf) or CSV-based statistical fitting**
- **Runtime configuration via JSON (no hardcoding)**
- **Multiple policy-duration pairs for scenario testing**

The simulator uses **SimPy** for discrete-event simulation and **SciPy** for statistical modeling.

---

## Features

### ✔ 1. Dynamic Distribution System
- Arrival & departure intervals are fitted automatically from **CSV** or **EasyFit .edf** files.
- Supports any SciPy distribution + EasyFit naming normalization.
- Final results saved into: src/config/distributions.json
- Simulation uses inverse CDF (PPF) for every lane:
```python
delay = get_inverse_cdf(dist_name, params, p)
```

### ✔ 2. Complete Adaptive Signal Controller
- Adjusts green durations based on lane pressure (mean delay).
- Fully compatible with fixed-time mode.
- Runs automatically in run_adaptive_simulation().

### ✔ 3. Config-Driven Architecture
No hardcoding. Everything is controlled by:
```python
src/config/
    policies.json
    durations.json
    distributions.json
    capacity.json
    init_conditions.json
```

### ✔ 4. Automated Validation Before Run
config_validator.py ensures all configs are consistent:
- Distribution param correctness
- Duration–phase length matching
- Capacity and initial queue structure
- Prevents runtime errors

---

## Project Structure
```python
adaptive-signal-control/
│
├── main.py
├── requirements.txt
│
├── src/
│   ├── simulation_core.py
│   ├── experiment.py
│   ├── lane.py
│   ├── light_control.py
│   ├── adaptive_light_control.py
│   ├── distributions_dynamic.py
│   ├── config_loader.py
│   ├── config_validator.py
│   │
│   ├── fitting/
│   │   ├── fit_distributions.py
│   │   ├── fit_all_distributions.py
│   │   ├── parse_edf.py
│   │   ├── export_to_config.py
│   │   ├── dataset_loader.py
│   │
│   └── config/
│       ├── policies.json
│       ├── durations.json
│       ├── capacity.json
│       ├── distributions.json
│       └── init_conditions.json
│
└── README.md
```

---

## Installation
1. Install Python packages

Windows PowerShell:

py -m pip install -r requirements.txt


Or manual install:

py -m pip install simpy scipy numpy pandas matplotlib

---

## How to Run Simulation
Fixed-Time Mode
```json
py main.py --mode fixed
```

Adaptive Mode
```json
py main.py --mode adaptive
```

Test All Scenarios
```json
py main.py --mode experiment
```

---

## Automatic Distribution Fitting
1. Fit from CSV datasets
Place CSV files in:
```bash
data/arrivals/
data/departures/
```
Then run:
```bash
py src/fitting/fit_all_distributions.py
```

2. Fit from EasyFit (.edf) files
Place EDF files in:
```bash
data/edf/
```
Run same command:
```bash
py src/fitting/fit_all_distributions.py
```

3. After fitting

Automatically updated to:
```bash
src/config/distributions.json
```

---

## Adaptive Signal Logic Summary

For each phase:
- Measure delay of involved lanes  
- Compute pressure  
- Identify most/least pressured lane groups  
- Shift green duration among phases  
- Update at end of every control cycle  

This algorithm is implemented inside:
```bash
AdaptiveLightControl.update_duration()
```

---

## Experiment Mode

You can run multiple policies × duration variations automatically:

- Each policy tested with dozens of duration combinations  
- Each experiment averaged over multiple seeds  
- Export results to CSV or terminal  

---

## Example distributions.json (after fitting)
```json
{
    "(1,2)_arr": { "dist": "lognorm", "params": [0.52, 0, 1.3] },
    "(1,2)_dep": { "dist": "gamma",   "params": [2.8, 0, 0.9] }
}
```
Simulation uses this dynamically—no code changes required.

---

## Development Notes

Every file has English comments for clarity.  
All parameters are externalized (config-based).  
Optional helper modules (fit_gev.py, etc.) were removed for clarity.

--- 

## Contribution
Contributions for bug fixes or feature improvements are always welcome!
Feel free to open an [Issue] or [Pull Request] to participate.

---

## Author
Seyoon Oh

Korea University — School of Industrial & Management Engineering

Email: osy7336@korea.ac.kr