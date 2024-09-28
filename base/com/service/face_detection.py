from bson import ObjectId
from base import app
from flask import jsonify,redirect,request
from base.com.service.face_recognition import facial_recognition
from base.com.service.model_train import train_model
from base.com.vo.student_vo import StudentVo
from base.com.vo.attendence_day_vo import AttendenceDayVo
from base.com.vo.attendence_vo import AttendenceVo
import os
from werkzeug.utils import secure_filename
import cv2
from datetime import datetime
import time
import mediapipe as mp


def face_detection(filepath):
    image = cv2.imread(filepath)

    # Load the image using OpenCV

    if image is None:
        os.remove(filepath)
        return jsonify({"message": "Could not read image"}), 400

    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Check if faces are detected
        if not results.detections:
            os.remove(filepath)
            return jsonify({"message": "No faces detected"}), 400

        # Annotate the image with detected faces
        annotated_image = image.copy()
        for detection in results.detections:
            print('Nose tip:')
            print(mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))

            # Draw face detections on the image
            mp_drawing.draw_detection(annotated_image, detection)
        # Save the uploaded file temporarily

        student_vo = StudentVo()

        student_vo.insert_student({
            "enrollment_no": enrollment_no,
            "full_name": full_name,
            "gender": gender,
            "age": age,
            "file_path": filepath
        })

    return jsonify({"message": "success"}), 200

    except Exception as ex:
        print(f"Exception: {ex}")
    return jsonify({"message": f"Error: {str(ex)}"}), 500