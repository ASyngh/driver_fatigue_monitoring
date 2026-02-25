import numpy as np
from modules.landmarks import RIGHT_EYE


def compute_ear(landmarks, w, h):
    coords = []

    for idx in RIGHT_EYE:
        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)
        coords.append((x, y))

    p1 = np.array(coords[0])
    p2 = np.array(coords[1])
    p3 = np.array(coords[2])
    p4 = np.array(coords[3])
    p5 = np.array(coords[4])
    p6 = np.array(coords[5])

    v1 = np.linalg.norm(p2 - p6)
    v2 = np.linalg.norm(p3 - p5)
    h_dist = np.linalg.norm(p1 - p4)

    ear = (v1 + v2) / (2.0 * h_dist)
    return ear