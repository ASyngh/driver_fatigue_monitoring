import numpy as np
from modules.landmarks import MOUTH


def compute_mar(landmarks, w, h):
    coords = []

    for idx in MOUTH:
        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)
        coords.append((x, y))

    p1 = np.array(coords[2])  # left corner
    p2 = np.array(coords[0])  # upper lip
    p3 = np.array(coords[4])  # upper inner
    p4 = np.array(coords[3])  # right corner
    p5 = np.array(coords[5])  # lower inner
    p6 = np.array(coords[1])  # lower lip

    v1 = np.linalg.norm(p2 - p6)
    v2 = np.linalg.norm(p3 - p5)
    h_dist = np.linalg.norm(p1 - p4)

    mar = (v1 + v2) / (2.0 * h_dist)
    return mar