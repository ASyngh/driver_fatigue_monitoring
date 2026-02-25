import time
import numpy as np


class Calibration:
    def __init__(self, duration=5):
        self.duration = duration
        self.start_time = None
        self.ear_values = []
        self.head_values = []
        self.calibrated = False

    def start(self):
        self.start_time = time.time()

    def update(self, ear, head_drop):
        if self.start_time is None:
            return

        if time.time() - self.start_time <= self.duration:
            self.ear_values.append(ear)
            self.head_values.append(head_drop)
        else:
            self.calibrated = True

    def get_thresholds(self):
        avg_ear = np.mean(self.ear_values)
        avg_head = np.mean(self.head_values)

        # Adaptive thresholds
        ear_threshold = avg_ear * 0.8
        head_threshold = avg_head + 7

        return ear_threshold, head_threshold