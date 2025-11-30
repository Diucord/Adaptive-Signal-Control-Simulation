"""
adaptive_light_control.py
---------------------------------
Adaptive signal controller.

After every full cycle:
- Measure "pressure" using lane delay averages
- Increase duration of the highest-pressure phase
- Decrease duration of the lowest-pressure phase
- Total cycle length stays constant
"""

import numpy as np
from .light_control import LightControl


class AdaptiveLightControl(LightControl):

    def __init__(self, env, policy, duration, dep_cycle, lane_list, log_enabled=True):
        """
        Extends LightControl with adaptive updates.
        """
        super().__init__(env, policy, duration, dep_cycle)
        self.lane_list = lane_list
        self.log_enabled = log_enabled
        self.duration_log = []

    def run_main_lights(self):
        """Override fixed-light cycle to insert duration update after each full cycle."""
        while True:
            for phase_index, phase in enumerate(self.policy):
                # Green
                for lane, d in phase:
                    self._broadcast(self.green_list[lane - 1][d - 1])
                yield self.env.timeout(self.duration[phase_index])

                # Red
                for lane, d in phase:
                    self._broadcast(self.red_list[lane - 1][d - 1])

            # After completing full cycle → update durations
            self.update_duration()

    def update_duration(self):
        """Adjust durations based on lane delay pressure."""
        pressure = []
        for i in range(4):
            for j in range(3):
                delays = self.lane_list[i][j].delay_list
                pressure.append(np.mean(delays) if delays else 0)

        # Identify phase with highest and lowest pressure
        max_i = np.argmax(pressure)
        min_i = np.argmin(pressure)

        # Convert flattened index to lane/direction
        def find_phase(idx):
            L = idx // 3 + 1
            D = idx % 3 + 1
            for pi, phase in enumerate(self.policy):
                if (L, D) in phase:
                    return pi
            return None

        high_phase = find_phase(max_i)
        low_phase  = find_phase(min_i)

        if high_phase is None or low_phase is None:
            return

        # Adjust durations
        if self.duration[high_phase] > 0:
            self.duration[high_phase] -= 1
            self.duration[low_phase] += 1

        # Log duration adjustment
        if self.log_enabled:
            self.duration_log.append(self.duration.copy())
