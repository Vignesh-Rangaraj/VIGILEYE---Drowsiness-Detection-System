import cv2
import dlib
import time
import face_recognition
import numpy as np

# Load known face images and corresponding names
known_face_encodings = []
known_face_names = [
    "SHAKTHI NATHAN S", 
    "SRI VISHNU MN"
]

known_images = [
    r"E:\EYE DET\Eye-Blink-Detector-Mine\assets\person1.jpg",
    r"E:\EYE DET\Eye-Blink-Detector-Mine\assets\person2.jpg",
]

# Load and encode all known images
for img_path in known_images:
    image = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(image)

    if encoding:  # Ensure encoding exists before adding
        known_face_encodings.append(encoding[0])

# Initialize camera
cam = cv2.VideoCapture(0)

# Load face detector and landmark model
detector = dlib.get_frontal_face_detector()
lm_model = dlib.shape_predictor(r"E:\EYE DET\Eye-Blink-Detector-Mine\Model\shape_predictor_68_face_landmarks.dat")

ptime = 0  # For FPS calculation

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Convert frame to RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations
    face_locations = face_recognition.face_locations(img_rgb)

    # Only compute encodings if faces are detected
    face_encodings = face_recognition.face_encodings(img_rgb, face_locations) if face_locations else []

    # Recognize faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # Draw bounding box and label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display FPS
    ctime = time.time()
    fps = 1 / (ctime - ptime) if ptime else 0
    ptime = ctime
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

    # Show the video feed
    cv2.imshow("Face Recognition", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cam.release()
cv2.destroyAllWindows()
