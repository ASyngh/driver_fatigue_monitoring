import mediapipe as mp
import cv2


class FaceDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def process(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        return results

    def draw(self, frame, face_landmarks):
        self.mp_drawing.draw_landmarks(
            frame,
            face_landmarks,
            self.mp_face_mesh.FACEMESH_TESSELATION
        )