import cv2
import mediapipe as mp
import numpy as np
import time
import winsound
import threading

from focus_tracker import FocusTracker
from utils import eye_aspect_ratio, head_pose_angle

# Initialize webcam and FocusTracker
cap = cv2.VideoCapture(0)
focus_tracker = FocusTracker()

# Mediapipe face mesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                   max_num_faces=1,
                                   refine_landmarks=True,
                                   min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5)

# Flags for managing beeping
beeping = False
beep_thread = None
stop_beep_flag = threading.Event()

# Function to continuously beep while distracted
def beep_loop():
    while not stop_beep_flag.is_set():
        winsound.Beep(1000, 300)
        time.sleep(0.1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape

            left_eye_indices = [33, 160, 158, 133, 153, 144]
            right_eye_indices = [362, 385, 387, 263, 373, 380]
            eye_points = []

            for i in left_eye_indices:
                x = int(landmarks.landmark[i].x * w)
                y = int(landmarks.landmark[i].y * h)
                eye_points.append((x, y))
            for i in right_eye_indices:
                x = int(landmarks.landmark[i].x * w)
                y = int(landmarks.landmark[i].y * h)
                eye_points.append((x, y))

            left_ear = eye_aspect_ratio(np.array(eye_points[:6]))
            right_ear = eye_aspect_ratio(np.array(eye_points[6:]))
            ear = (left_ear + right_ear) / 2.0

            nose_idx = 1
            chin_idx = 152
            nose = (int(landmarks.landmark[nose_idx].x * w), int(landmarks.landmark[nose_idx].y * h))
            chin = (int(landmarks.landmark[chin_idx].x * w), int(landmarks.landmark[chin_idx].y * h))
            angle = head_pose_angle(nose, chin)

            print(f"EAR: {ear:.2f}, Head Angle: {angle:.2f}")

            if ear < 0.20 or not (80 <= angle <= 100):
                focus_tracker.distracted_score += 1
                focus_tracker.focus_score = max(0, focus_tracker.focus_score - 1)
            else:
                focus_tracker.focus_score += 1
                focus_tracker.distracted_score = max(0, focus_tracker.distracted_score - 1)

            focus_tracker.distracted_score = min(focus_tracker.distracted_score, 100)
            focus_tracker.focus_score = min(focus_tracker.focus_score, 100)

            cv2.putText(frame, f"Distraction Score: {focus_tracker.distracted_score}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f"Focus Score: {focus_tracker.focus_score}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

            # Check if user is distracted
            if focus_tracker.is_distracted() and focus_tracker.focus_score < 40:
                cv2.putText(frame, "You are Distracted!", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Start beeping if not already
                if not beeping:
                    stop_beep_flag.clear()
                    beep_thread = threading.Thread(target=beep_loop, daemon=True)
                    beep_thread.start()
                    beeping = True
            else:
                # Stop beeping if focus is regained
                if beeping:
                    stop_beep_flag.set()
                    if beep_thread:
                        beep_thread.join(timeout=0.2)
                    beeping = False

    cv2.imshow('FocusSense - Distraction Tracker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        stop_beep_flag.set()
        break

cap.release()
cv2.destroyAllWindows()
