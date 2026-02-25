from playsound import playsound
import threading
import os


class AlertSystem:
    def __init__(self):
        self.prev_state = "NORMAL"
        self.base_path = os.path.join(os.getcwd(), "assets")

    def _play(self, filename):
        filepath = os.path.join(self.base_path, filename)
        threading.Thread(
            target=playsound,
            args=(filepath,),
            daemon=True
        ).start()

    def update(self, fatigue_state):
        # Trigger only on state change
        if fatigue_state != self.prev_state:

            if fatigue_state == "WARNING":
                self._play("warning.wav")

            elif fatigue_state == "CRITICAL":
                self._play("critical.wav")

        self.prev_state = fatigue_state