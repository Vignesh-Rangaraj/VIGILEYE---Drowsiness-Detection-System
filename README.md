
EYE-DET – Drowsiness Detection System
-------------------------------------

A Python and OpenCV based real-time system for detecting eye closure, blinking patterns, and drowsiness using facial landmark analysis and Eye Aspect Ratio (EAR).

-------------------------------------
PROJECT OVERVIEW
-------------------------------------
EYE-DET monitors a user's eye activity through a webcam or video feed. It detects when the user is becoming drowsy by analyzing the eye aspect ratio over consecutive frames. If the eyes remain closed beyond a threshold, the system identifies drowsiness and triggers an alert.

-------------------------------------
FEATURES
-------------------------------------
- Real-time eye detection
- Detects blinking and long eye closure
- Drowsiness detection using EAR logic
- Works with webcam, image, or video
- Lightweight and easy to run
- Highly configurable threshold values

-------------------------------------
HOW IT WORKS
-------------------------------------
The system uses eye landmarks from the detected face and computes the Eye Aspect Ratio (EAR).

EAR Formula:
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)

Where p1 to p6 represent key eye landmark points.

Logic:
- If EAR < 0.25 → Eyes Closed
- If EAR < 0.25 for 20+ frames → Drowsiness Detected

You can adjust threshold and frame count based on environment and camera quality.

-------------------------------------
TECH STACK
-------------------------------------
- Python 3.7+
- OpenCV
- Numpy
- Scipy
- Imutils
- Dlib / Haarcascade (based on implementation)

-------------------------------------
PROJECT STRUCTURE
-------------------------------------
EYE-DET/
  public/
    basic.py        - Basic eye detection script
    new.py          - Main drowsiness detection system
    README.md
  models/           - (Optional) Face/eye detection models
  src/              - (Optional) Additional logic and utilities
  requirements.txt  - Required Python libraries
  README.md         - Main project documentation

-------------------------------------
INSTALLATION
-------------------------------------
1. Clone the repository:
   git clone https://github.com/Vignesh-Rangaraj/EYE-DET.git
   cd EYE-DET

2. Install dependencies:
   pip install -r requirements.txt

3. Run the main script:
   python public/new.py

-------------------------------------
USAGE
-------------------------------------
Run with webcam:
   python public/new.py --webcam

Run on an image:
   python public/new.py --image sample.jpg

Run on a video:
   python public/new.py --video input.mp4

-------------------------------------
REQUIREMENTS
-------------------------------------
- Python 3.7 or higher
- OpenCV
- Imutils
- Numpy
- Scipy
- Dlib (optional, if used for landmarks)

-------------------------------------
FUTURE ENHANCEMENTS
-------------------------------------
- Sound alarm alerts
- UI dashboard
- ML-based eye-state classifier
- Mobile version using Flutter + Mediapipe
- Advanced driver monitoring system

-------------------------------------
AUTHOR
-------------------------------------
Developed by: Vignesh Rangaraj
GitHub Repo: https://github.com/Vignesh-Rangaraj/EYE-DET

-------------------------------------
LICENSE
-------------------------------------
This project is licensed under the MIT License.
