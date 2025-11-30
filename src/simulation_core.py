"""
simulation_core.py
------------------------
Provides:
- run_fixed(): run simulation with fixed schedule
- run_adaptive(): run simulation with adaptive controller
"""

import simpy
import random
from .lane import Lane, capacity_matrix
from .light_control import LightControl
from .config_loader import load_json
from .lane import get_arr_time


def gen_cars(env, lane, i, j, arr_duration):
    """
    Generate arriving vehicles according to the arrival distribution.
    """
    green, red = arr_duration[i]
    cycle = green + red

    while True:
        # Check if upstream signal is red
        if (env.now + 60) % cycle > green:
            extra = 0
            if len(lane.lane_q) < 15:
                extra = (15 - len(lane.lane_q)) * 2.5
            jump = cycle - env.now % cycle + extra
            yield env.timeout(jump)

        else:
            delay = get_arr_time(random.random(), i, j)
            yield env.timeout(delay)
            lane.add_car(object())


def _build_lanes(env):
    """
    Helper: create all Lane objects for the intersection.
    """
    types = ["East", "South", "West", "North"]
    dirs = ["left", "straight", "right"]

    lane_list = [
        [Lane(f"{types[i]} {dirs[j]}", env, i, j, capacity_matrix[i][j]) for j in range(3)]
        for i in range(4)
    ]

    return lane_list


def run_fixed(policy, duration, runtime, seed):
    """
    Run fixed scheduling simulation.
    """
    random.seed(seed)
    env = simpy.Environment()

    lane_list = _build_lanes(env)

    dep_cycle = load_json("capacity.json")["departure_cycle"]
    arr_duration = load_json("capacity.json")["departure_cycle"]

    # Create controller
    ctl = LightControl(env, policy, duration, dep_cycle)

    # Register callbacks
    for i in range(4):
        for j in range(3):
            ctl.green_list[i][j].append(lane_list[i][j].green_light)
            ctl.red_list[i][j].append(lane_list[i][j].red_light)

    # Car generators
    for i in range(4):
        for j in range(3):
            if (i, j) in [(0, 0), (2, 0)]:
                continue
            env.process(gen_cars(env, lane_list[i][j], i, j, arr_duration))

    env.run(runtime)

    # Compute performance
    total_delay = 0
    total_cust = 0

    for i in range(4):
        for j in range(3):
            if (i, j) in [(0, 0), (2, 0)]:
                continue
            total_delay += lane_list[i][j].total_delay
            total_cust  += lane_list[i][j].total_customer

    return total_delay / total_cust
