import cv2
import numpy as np


def apply_clahe(frame, brightness_threshold=80):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    avg_brightness = np.mean(gray)

    if avg_brightness < brightness_threshold:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

    # If brightness is sufficient → return original frame
    return frame