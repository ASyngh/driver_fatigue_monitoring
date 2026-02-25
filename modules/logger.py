import csv
import time
import os


class SessionLogger:
    def __init__(self):
        self.session_start_time = time.time()

        self.eye_events = 0
        self.yawn_events = 0
        self.head_droop_events = 0
        self.critical_events = 0

        # Track previous state to detect transitions
        self.prev_eye_state = False
        self.prev_yawn_state = False
        self.prev_head_state = False
        self.prev_critical_state = False

    def update(self, eye_flag, yawn_flag, head_flag, fatigue_state):
        # Eye event detection (False → True)
        if eye_flag and not self.prev_eye_state:
            self.eye_events += 1

        if yawn_flag and not self.prev_yawn_state:
            self.yawn_events += 1

        if head_flag and not self.prev_head_state:
            self.head_droop_events += 1

        if fatigue_state == "CRITICAL" and not self.prev_critical_state:
            self.critical_events += 1

        # Update previous states
        self.prev_eye_state = eye_flag
        self.prev_yawn_state = yawn_flag
        self.prev_head_state = head_flag
        self.prev_critical_state = (fatigue_state == "CRITICAL")

    def end_session(self):
        duration = int(time.time() - self.session_start_time)

        summary = {
            "duration_seconds": duration,
            "eye_closure_events": self.eye_events,
            "yawn_events": self.yawn_events,
            "head_droop_events": self.head_droop_events,
            "critical_fatigue_events": self.critical_events
        }

        return summary

    def save_to_csv(self, summary, filepath="logs/session_logs.csv"):
        os.makedirs("logs", exist_ok=True)

        file_exists = os.path.isfile(filepath)

        with open(filepath, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=summary.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(summary)