import cv2

from config import (
    EAR_THRESHOLD as DEFAULT_EAR_THRESHOLD,
    EAR_CONSEC_FRAMES,
    MAR_THRESHOLD,
    MAR_CONSEC_FRAMES,
    HEAD_DROP_THRESHOLD as DEFAULT_HEAD_DROP_THRESHOLD,
    HEAD_DROP_CONSEC_FRAMES
)

from modules.face_detector import FaceDetector
from modules.preprocessing import apply_clahe
from modules.eye_analysis import compute_ear
from modules.mouth_analysis import compute_mar
from modules.head_pose import compute_head_drop
from modules.fatigue_logic import evaluate_fatigue
from modules.logger import SessionLogger
from modules.display import draw_text, draw_fatigue_state
from modules.alert import AlertSystem
from modules.calibration import Calibration


def main():
    cap = cv2.VideoCapture(0)

    detector = FaceDetector()
    logger = SessionLogger()
    alert_system = AlertSystem()

    # Use mutable thresholds (will be updated after calibration)
    EAR_THRESHOLD = DEFAULT_EAR_THRESHOLD
    HEAD_DROP_THRESHOLD = DEFAULT_HEAD_DROP_THRESHOLD

    eye_counter = 0
    mouth_counter = 0
    head_counter = 0

    eye_closed_flag = False
    yawn_flag = False
    head_droop_flag = False

    # ======================
    # AUTO CALIBRATION SETUP
    # ======================
    calibration = Calibration(duration=5)
    calibration.start()
    calibrated = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = apply_clahe(frame)

        results = detector.process(frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:

                detector.draw(frame, face_landmarks)

                landmarks = face_landmarks.landmark
                h, w, _ = frame.shape

                # ======================
                # COMPUTE FEATURES
                # ======================
                head_drop = compute_head_drop(landmarks, w, h)
                mar = compute_mar(landmarks, w, h)
                ear = compute_ear(landmarks, w, h)

                # ======================
                # CALIBRATION PHASE
                # ======================
                if not calibration.calibrated:
                    calibration.update(ear, head_drop)

                    draw_text(
                        frame,
                        "CALIBRATING... Keep head straight & eyes open",
                        (30, 280),
                        (0, 255, 255),
                        0.7
                    )

                else:
                    if not calibrated:
                        EAR_THRESHOLD, HEAD_DROP_THRESHOLD = calibration.get_thresholds()
                        calibrated = True

                        print("Calibration Complete")
                        print("New EAR_THRESHOLD:", EAR_THRESHOLD)
                        print("New HEAD_DROP_THRESHOLD:", HEAD_DROP_THRESHOLD)

                    # ======================
                    # HEAD DROP LOGIC
                    # ======================
                    if head_drop > HEAD_DROP_THRESHOLD:
                        head_counter += 1
                    else:
                        head_counter = 0

                    head_droop_flag = head_counter >= HEAD_DROP_CONSEC_FRAMES

                    # ======================
                    # YAWN LOGIC
                    # ======================
                    if mar > MAR_THRESHOLD:
                        mouth_counter += 1
                    else:
                        mouth_counter = 0

                    yawn_flag = mouth_counter >= MAR_CONSEC_FRAMES

                    # ======================
                    # EYE CLOSURE LOGIC
                    # ======================
                    if ear < EAR_THRESHOLD:
                        eye_counter += 1
                    else:
                        eye_counter = 0

                    eye_closed_flag = eye_counter >= EAR_CONSEC_FRAMES

                    # ======================
                    # FATIGUE FUSION
                    # ======================
                    fatigue_state, fatigue_score = evaluate_fatigue(
                        eye_closed_flag,
                        yawn_flag,
                        head_droop_flag
                    )

                    alert_system.update(fatigue_state)

                    logger.update(
                        eye_closed_flag,
                        yawn_flag,
                        head_droop_flag,
                        fatigue_state
                    )

                    draw_fatigue_state(frame, fatigue_state)

                # Always show raw metrics
                draw_text(frame, f"EAR: {ear:.3f}", (30, 40), (0, 255, 0), 0.8)
                draw_text(frame, f"MAR: {mar:.2f}", (30, 110), (255, 255, 0))
                draw_text(frame, f"HeadDrop: {head_drop:.2f}", (30, 170), (255, 0, 255))

        cv2.imshow("Driver Fatigue Monitoring", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    summary = logger.end_session()
    logger.save_to_csv(summary)

    print("Session Summary:", summary)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()