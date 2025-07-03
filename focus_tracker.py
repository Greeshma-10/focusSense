import numpy as np
from utils import eye_aspect_ratio, head_pose_angle

class FocusTracker:
    def __init__(self):
        self.distracted_score = 0
        self.focused_score = 0
        self.focus_score = 100
        self.focus_threshold = 60
        self.blink_threshold = 0.21  # Lowered to match actual EAR range
        self.head_angle_threshold = 25  # Head tilt angle (degrees)

        # Correct landmark indices
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]
        self.NOSE_IDX = 1
        self.CHIN_IDX = 152

    def get_eye_coordinates(self, landmarks, frame_shape, side="left"):
        h, w = frame_shape[:2]
        indices = self.LEFT_EYE if side == "left" else self.RIGHT_EYE
        return [(int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h)) for i in indices]

    def get_head_coordinates(self, landmarks, frame_shape):
        h, w = frame_shape[:2]
        nose = (int(landmarks.landmark[self.NOSE_IDX].x * w),
                int(landmarks.landmark[self.NOSE_IDX].y * h))
        chin = (int(landmarks.landmark[self.CHIN_IDX].x * w),
                int(landmarks.landmark[self.CHIN_IDX].y * h))
        return nose, chin

    def update_focus_score(self, landmarks, frame):
        left_eye = self.get_eye_coordinates(landmarks, frame.shape, "left")
        right_eye = self.get_eye_coordinates(landmarks, frame.shape, "right")
        nose, chin = self.get_head_coordinates(landmarks, frame.shape)

        # Calculate average EAR from both eyes
        left_ear = eye_aspect_ratio(np.array(left_eye))
        right_ear = eye_aspect_ratio(np.array(right_eye))
        ear = (left_ear + right_ear) / 2.0

        head_angle = head_pose_angle(nose, chin)

        # Debug prints (optional)
        # print(f"EAR: {ear:.3f}, Head Angle: {head_angle:.2f}")

        if ear < self.blink_threshold:
            self.distracted_score += 5  # Blink
        if abs(head_angle) > self.head_angle_threshold:
            self.distracted_score += 5  # Tilted head

        # If focused, reduce distraction
        if ear >= self.blink_threshold and abs(head_angle) <= self.head_angle_threshold:
            self.distracted_score = max(self.distracted_score - 10, 0)

        # Clamp and update focus score
        self.focus_score = max(0, min(100, 100 - self.distracted_score))

    def is_distracted(self):
        return self.focus_score < self.focus_threshold
