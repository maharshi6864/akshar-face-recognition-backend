from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import numpy as np
from PIL import Image

from base.com.vo.attendence_vo import AttendenceVo
from base.com.vo.student_vo import StudentVo


def facial_recognition():
    # initialize 'currentname' to trigger only when a new person is identified
    currentname = "unknown"
    student_dao = StudentVo()
    attendence_dao = AttendenceVo()
    # determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings.pickle"
    # use this xml file
    cascade = "C:/Users/MAHARSHI_PATEL/Desktop/Akshar_fullStack/askhar-python/akshar-face-recognition-backend/base/com/service/haarcascade_frontalface_default.xml"
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())
    detector = cv2.CascadeClassifier(cascade)

    if image is None:
        print(f"Error: Unable to load image at ")
        continue

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb, model="hog")

    # Compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

    # Loop over the encodings
    for encoding in encodings:
        # Add each encoding + name to our set of known names and encodings
        knownEncodings.append(encoding)
        knownNames.append(name)

    # Dump the facial encodings + names to disk


    print("[INFO] serializing encodings...")
    file_path = os.path.abspath("encodings.pickle")
    print(f"[INFO] Encodings will be saved at: {file_path}")

# Save the updated encodings
    save_encodings(file_path, knownEncodings, knownNames)