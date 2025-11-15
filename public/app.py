from flask import Flask, send_from_directory
import subprocess
import os

app = Flask(__name__)

SCRIPT_PATH = r"E:\MINI PROJECT\EYE DET\public"

@app.route('/')
def home():
    return send_from_directory(SCRIPT_PATH, 'success.html')

@app.route('/start-drowsiness')
def start_drowsiness():
    try:
        subprocess.run(["python", os.path.join(SCRIPT_PATH, "basic.py")])
        return "Drowsiness Detection Started!", 200
    except Exception as e:
        return str(e), 500

@app.route('/start-face-detection')
def start_face_detection():
    try:
        subprocess.run(["python", os.path.join(SCRIPT_PATH, "facedetect.py")])
        return "Face Detection Started!", 200
    except Exception as e:
        return str(e), 500

@app.route('/view-existing')
def view_existing():
    try:
        subprocess.run(["python", os.path.join(SCRIPT_PATH, "new.py")])
        return "Displaying Existing Detection Videos!", 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
