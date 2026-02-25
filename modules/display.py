import cv2


def draw_text(frame, text, position, color=(0, 255, 0), scale=0.7):
    cv2.putText(frame, text, position,
                cv2.FONT_HERSHEY_SIMPLEX,
                scale, color, 2)


def draw_fatigue_state(frame, state):
    color = (0, 255, 0) if state == "NORMAL" else (0, 0, 255)

    cv2.putText(frame,
                f"Fatigue: {state}",
                (30, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2)