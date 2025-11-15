import cv2
import dlib
import imutils
import winsound
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils

# Initialize webcam
cam = cv2.VideoCapture(0)

# EAR calculation
def calculate_EAR(eye):
    if len(eye) < 6:
        return 1
    y1 = dist.euclidean(eye[1], eye[5])
    y2 = dist.euclidean(eye[2], eye[4])
    x1 = dist.euclidean(eye[0], eye[3])
    return (y1 + y2) / (2.0 * x1)

# MAR calculation
def calculate_MAR(mouth):
    y1 = dist.euclidean(mouth[2], mouth[10])
    y2 = dist.euclidean(mouth[4], mouth[8])
    x1 = dist.euclidean(mouth[0], mouth[6])
    return (y1 + y2) / (2.0 * x1)

# Equalize brightness
def equalize_brightness(gray_frame):
    return cv2.equalizeHist(gray_frame)

# Draw landmarks
def draw_face_landmarks(frame, shape):
    for (x, y) in shape:
        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
    for (i, j) in face_utils.FACIAL_LANDMARKS_IDXS.values():
        cv2.polylines(frame, [shape[i:j]], isClosed=False, color=(255, 255, 0), thickness=1)

# Constants
default_blink_thresh = 0.25
mar_thresh = 0.6
succ_frame = 20  # Threshold frame count for sustained alert

eye_frame = 0
mouth_frame = 0

# Dlib setup
detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor(r'E:\EYE DET\Eye-Blink-Detector-Mine\Model\shape_predictor_68_face_landmarks.dat')

(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(M_start, M_end) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# EAR calibration
baseline_ear = []
calibration_frames = 30

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=720)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = equalize_brightness(gray)

    faces = detector(gray)
    for face in faces:
        shape = landmark_predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        draw_face_landmarks(frame, shape)

        lefteye = shape[L_start:L_end]
        righteye = shape[R_start:R_end]
        mouth = shape[M_start:M_end]

        left_EAR = calculate_EAR(lefteye)
        right_EAR = calculate_EAR(righteye)
        avg_EAR = (left_EAR + right_EAR) / 2
        mar = calculate_MAR(mouth)

        # Calibration phase
        if len(baseline_ear) < calibration_frames:
            baseline_ear.append(avg_EAR)
            continue

        blink_thresh = max(0.75 * np.mean(baseline_ear), default_blink_thresh)

        # EAR counter
        if avg_EAR < blink_thresh:
            eye_frame += 1
        else:
            eye_frame = 0

        # MAR counter
        if mar > mar_thresh:
            mouth_frame += 1
        else:
            mouth_frame = 0

        # Trigger alert only if one of them is consistently flagged
        if eye_frame >= succ_frame or mouth_frame >= succ_frame:
            cv2.putText(frame, "DROWSINESS ALERT!", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)
            winsound.Beep(1000, 500)

        # Show EAR & MAR
        cv2.putText(frame, f"EAR: {avg_EAR:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, f"MAR: {mar:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow("Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
