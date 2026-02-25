from modules.landmarks import NOSE_TIP, LEFT_EYE_OUTER, RIGHT_EYE_OUTER


def compute_head_drop(landmarks, w, h):
    nose_y = landmarks[NOSE_TIP].y * h
    left_eye_y = landmarks[LEFT_EYE_OUTER].y * h
    right_eye_y = landmarks[RIGHT_EYE_OUTER].y * h

    eye_center_y = (left_eye_y + right_eye_y) / 2.0

    head_drop_value = nose_y - eye_center_y

    return head_drop_value