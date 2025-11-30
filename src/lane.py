"""
lane.py
-----------------
Lane model for the intersection.

Each lane contains:
- FIFO queue of vehicles
- timestamps of arrival
- dynamic delay calculation
- movement to departure queue
"""

import random
from .config_loader import load_json
from .distributions_dynamic import get_inverse_cdf

# Load configs
dist_cfg = load_json("distributions.json")
init_cfg = load_json("init_conditions.json")
capacity_cfg = load_json("capacity.json")

capacity_matrix = capacity_cfg["capacity"]
dep_capacity = capacity_cfg["departure_capacity"]
dep_cycle = capacity_cfg["departure_cycle"]

# Departure queue (shared)
dep_queue = [0, 0, 0, 0]
dep_vanish = [cycle[0] // 1 for cycle in dep_cycle]  # cars that disappear during red


def get_arr_time(p, i, j):
    """Return inverse CDF for arrival distribution of lane (i,j)."""
    key = f"({i+1},{j+1})_arr"
    d = dist_cfg[key]
    return get_inverse_cdf(d["dist"], d["params"], p)


def get_dep_time(p, i, j):
    """Return inverse CDF for departure distribution of lane (i,j)."""
    key = f"({i+1},{j+1})_dep"
    d = dist_cfg[key]
    return get_inverse_cdf(d["dist"], d["params"], p)


class Lane:
    def __init__(self, name, env, i, j, capacity):
        self.name = name
        self.env = env
        self.i = i
        self.j = j
        self.capacity = capacity

        self.lane_q = []
        self.time_q = []
        self.green = False

        self.dep_lane = (i + j) % 4

        self.total_customer = 0
        self.total_delay = 0
        self.delay_list = []

    def add_car(self, car):
        """Add a car to the lane queue or pass immediately if green."""
        if self.green and not self.lane_q:
            self.total_customer += 1
            self.delay_list.append(0)
        else:
            if len(self.lane_q) < self.capacity:
                self.lane_q.append(car)
                self.time_q.append(self.env.now)

    def move_cars(self):
        """Move cars from this lane to the departure lane."""
        while self.green and self.lane_q:

            # If departure lane is full → wait
            if dep_queue[self.dep_lane] > dep_capacity[self.dep_lane]:
                yield self.env.timeout(1)
                continue

            car = self.lane_q.pop(0)
            t = self.time_q.pop(0)

            dep_queue[self.dep_lane] += 1

            delay = self.env.now - t

            # Ignore initial dummy cars
            init_count = init_cfg.get(f"({self.i+1},{self.j+1})", 0)
            if self.total_customer < init_count:
                delay = 0

            self.total_customer += 1
            self.total_delay += delay
            self.delay_list.append(delay)

            dep_delay = get_dep_time(random.random(), self.i, self.j)
            yield self.env.timeout(dep_delay)

    def green_light(self):
        """Callback when this lane receives green."""
        self.green = True
        self.env.process(self.move_cars())

    def red_light(self):
        """Callback when this lane receives red."""
        self.green = False
