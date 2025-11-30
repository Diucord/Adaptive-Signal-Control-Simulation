"""
light_control.py
----------------------
Fixed-schedule traffic signal controller.

This module handles:
- Broadcasting green/red light events to lanes
- Cycle-based timing for each policy phase
- Departure lane clearance (departure queue behavior)

Used by both fixed and adaptive simulations.
"""

from .lane import dep_queue, dep_vanish


class LightControl:
    def __init__(self, env, policy, duration, dep_cycle):
        """
        Args:
            env (simpy.Environment)
            policy (list): list of phases, each phase is list of (lane, dir)
            duration (list): green duration for each phase
            dep_cycle (list): departure lane signal cycle (green/red)
        """
        self.env = env
        self.policy = policy
        self.duration = duration
        self.dep_cycle = dep_cycle

        # Create green/red light subscriber lists
        self.green_list = [[[] for _ in range(3)] for _ in range(4)]
        self.red_list   = [[[] for _ in range(3)] for _ in range(4)]

        # Start light processes
        env.process(self.run_main_lights())
        env.process(self.run_departure_lights())

    def _broadcast(self, subscribers):
        """Trigger all registered callbacks (lane.green_light / red_light)."""
        for callback in subscribers:
            callback()

    def run_main_lights(self):
        """Run the fixed green durations for each phase."""
        while True:
            for phase_index, phase in enumerate(self.policy):

                # Activate all lanes in this phase
                for lane, d in phase:
                    self._broadcast(self.green_list[lane - 1][d - 1])

                # Keep lights green for specified duration
                yield self.env.timeout(self.duration[phase_index])

                # Turn red for all lanes in this phase
                for lane, d in phase:
                    self._broadcast(self.red_list[lane - 1][d - 1])

    def run_departure_lights(self):
        """
        Departure lane behavior:
        - Red time: clear vanishing queue
        - Green time: vehicles freely disappear (no blocking)
        """
        while True:
            for lane in range(4):
                red_t, green_t = self.dep_cycle[lane]

                # Red time → departure queue is reduced
                yield self.env.timeout(red_t)
                if dep_queue[lane] < dep_vanish[lane]:
                    dep_queue[lane] = 0
                else:
                    dep_queue[lane] -= dep_vanish[lane]

                # Green time
                yield self.env.timeout(green_t)
