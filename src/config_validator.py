"""
config_validator.py
------------------------------------
Validation utilities for all configuration JSON files.

This module ensures that:
- duration sets match the number of policy phases
- distributions.json entries are correctly formatted
- required keys exist in each config

It prevents runtime errors arising from malformed config files.
"""


def validate_duration(policy, duration):
    """
    Ensure duration list length == number of policy phases.

    Args:
        policy (list): List of phases (e.g., [[(1,2),(1,3)], ...])
        duration (list): Green time for each phase

    Raises:
        ValueError: Duration length mismatch
    """
    if len(policy) != len(duration):
        raise ValueError(
            f"Duration length mismatch: "
            f"policy has {len(policy)} phases but duration has {len(duration)} values."
        )


def validate_distributions(dist_cfg):
    """
    Validate that each distribution entry contains:
    - "dist": distribution name
    - "params": list of numerical parameters

    Args:
        dist_cfg (dict): loaded distributions.json

    Raises:
        ValueError: if any entry is malformed
    """
    for key, entry in dist_cfg.items():
        if "dist" not in entry:
            raise ValueError(f"Distribution entry '{key}' missing 'dist' field.")

        if "params" not in entry:
            raise ValueError(f"Distribution entry '{key}' missing 'params' field.")

        if not isinstance(entry["params"], (list, tuple)):
            raise ValueError(f"'params' for '{key}' must be a list or tuple.")

        for p in entry["params"]:
            if not isinstance(p, (int, float)):
                raise ValueError(
                    f"Invalid parameter type in '{key}': all params must be numeric."
                )


def validate_capacity(cap_cfg):
    """
    Validate structure of capacity.json.

    Expected keys:
    - "capacity" (4x3 matrix)
    - "departure_capacity" (list of size 4)
    - "departure_cycle" (list of 4 [red, green] pairs)

    Raises:
        ValueError if structure is invalid.
    """
    if "capacity" not in cap_cfg:
        raise ValueError("capacity.json missing 'capacity'.")

    if "departure_capacity" not in cap_cfg:
        raise ValueError("capacity.json missing 'departure_capacity'.")

    if "departure_cycle" not in cap_cfg:
        raise ValueError("capacity.json missing 'departure_cycle'.")

    if len(cap_cfg["capacity"]) != 4:
        raise ValueError("capacity must have 4 lane groups (East/South/West/North).")

    for row in cap_cfg["capacity"]:
        if len(row) != 3:
            raise ValueError("capacity row must have 3 columns (left/straight/right).")

    if len(cap_cfg["departure_capacity"]) != 4:
        raise ValueError("'departure_capacity' must contain 4 elements.")

    if len(cap_cfg["departure_cycle"]) != 4:
        raise ValueError("'departure_cycle' must have 4 entries.")

    for cycle in cap_cfg["departure_cycle"]:
        if len(cycle) != 2:
            raise ValueError("Each departure cycle must have [red, green] pair.")


def validate_init_conditions(init_cfg):
    """
    Validate initial queue conditions.

    Key format: "(i,j)" where i=1..4, j=1..3
    Value: integer or null

    Args:
        init_cfg (dict)

    Raises:
        ValueError
    """
    for key, value in init_cfg.items():
        if not (key.startswith("(") and key.endswith(")")):
            raise ValueError(f"Invalid key format in init_conditions: {key}")

        # Validate number inside
        try:
            i, j = key.strip("()").split(",")
            i = int(i)
            j = int(j)
        except:
            raise ValueError(f"Invalid lane id '{key}' in init_conditions.")

        if value is not None and not isinstance(value, int):
            raise ValueError(f"Initial count for '{key}' must be int or null.")


def validate_all(cfg):
    """
    Validate all configuration files.

    Args:
        cfg (dict):
            {
                "base": ...,
                "durations": ...,
                "policies": ...,
                "dists": ...,
                "init": ...,
                "caps": ...
            }
    """
    print("[VALIDATOR] Validating all configuration files...")

    # Duration & policies
    durations_list = cfg["durations"]
    policy_list = cfg["policies"]

    for i in range(len(durations_list)):
        policy = policy_list[i] if i < len(policy_list) else policy_list[0]
        validate_duration(policy, durations_list[i])

    # Distributions
    validate_distributions(cfg["dists"])

    # Capacity
    validate_capacity(cfg["caps"])

    # Init conditions
    validate_init_conditions(cfg["init"])

    print("[VALIDATOR] All config files are valid.\n")
