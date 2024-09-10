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

face_images_path = 'base/static/face_images/'
app.config['FACE_IMAGES'] = face_images_path

@app.route('/hello')
def hello():
   
    # Create a dictionary with the data you want to return as JSON
    response_data = {
        "message": "Hello World! This is me",
        "status": "success"
    }
    
    # Return the JSON response along with a status code (e.g., 200 for OK)
    return jsonify(response_data), 200  # 200 is the HTTP status code for success


@app.route('/train', methods=["POST"])
def train():
  #  Write Train Model code :
    student_dao=StudentVo()
    data = request.get_json()  # Get the JSON data from the request
    student_model_train_list=data['student_list']
    image_paths=[]
    student_id_list=[]
    for  i in range(len(student_model_train_list)):
        student_vo=student_model_train_list[i]
        student_to_train=student_dao.find_student_by_id(student_vo['_id'])
        image_path=student_to_train['file_path']
        student_id_list.append(student_vo['_id'])
        image_paths.append(image_path)
    train_model(image_paths,student_id_list)
        


    response_data = {
        "message": "success",
    }

    return jsonify(response_data), 200

@app.route('/test')
def test():
  #  Write Test Model code :
    facial_recognition()

    response_data = {
        "message": "success",
        "status":"true"
    }
    
    return jsonify(response_data), 200

@app.route('/getStudents')
def getStudents():
    try:
        student_vo = StudentVo()
        attendence_day_vo=AttendenceDayVo()

        students_list = student_vo.list_students()

        date_time = datetime.fromtimestamp(time.time())
        year = date_time.strftime("%Y")
        date = date_time.strftime("%d")
        month = date_time.strftime("%m")
        today = datetime(int(year), int(month), int(date), 0, 0, 0)

        today_timestamp = today.timestamp()

        attendence_day_vo_for_today=attendence_day_vo.find_attendence_by_timestamp(today_timestamp)
        attendence_day_id=0
        if attendence_day_vo_for_today is None:
             print("in if")
             print(attendence_day_vo_for_today)
             attendence_day_id=attendence_day_vo.insert_attendence_for_day({
            "timestamp":today_timestamp
        }).inserted_id
        else :
            attendence_day_id=attendence_day_vo_for_today['_id']
       
        
        for student in students_list:
            attendence_vo=AttendenceVo()
            if attendence_day_vo_for_today is None:
                 attendence_vo_id=attendence_vo.insert_attendence({
                "attendence_marked_timestamp":today_timestamp,
                "student_id":str(student['_id']),
                "status":"absent",
                "attendence_day_id":str(attendence_day_id)
                    }).inserted_id
                 if '_id' in student:
                    student['_id'] = str(student['_id'])
                    attendence_vo=attendence_vo.find_one(attendence_vo_id)
                    attendence_vo['_id']=str(attendence_vo['_id'])
                    student['attendence_vo']=attendence_vo
            else:
                if '_id' in student:
                    student['_id'] = str(student['_id'])
                    attendence_vo= attendence_vo.find_one_by_student_id(str(student['_id']))
                    if attendence_vo is None:
                        attendence_vo_new=AttendenceVo()
                        attendence_vo_id=attendence_vo_new.insert_attendence({
                            "attendence_marked_timestamp":today_timestamp,
                            "student_id":str(student['_id']),
                            "status":"absent",
                            "attendence_day_id":str(attendence_day_id)
                                }).inserted_id
                        attendence_vo= attendence_vo_new.find_one_by_student_id(str(student['_id']))
                    attendence_vo['_id']=str(attendence_vo['_id'])
                    student['attendence_vo']=attendence_vo
        response_data = {
              "message": "success",
            "students": students_list,
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Failed to retrieve students"}), 500


@app.route('/register-student', methods=["POST"])
def register_student():
    try:
        # Capture form data
        enrollment_no = request.form.get('enrollment_no')
        full_name = request.form.get('full_name')
        gender = request.form.get('gender')
        age = request.form.get('age')

        # Handle file upload
        file = request.files.get('face_image')
        if not file:
            return jsonify({"message": "No file uploaded"}), 400
        
        # Save the uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['FACE_IMAGES'],filename)
        file.save(filepath)

        # Load the image using OpenCV
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
            
            student_vo=StudentVo()

            student_vo.insert_student({
                "enrollment_no":enrollment_no,
                "full_name":full_name,
                "gender":gender,
                "age":age,
                "file_path":filepath
            })
            
        return jsonify({"message": "success"}), 200

    except Exception as ex:
        print(f"Exception: {ex}")
        return jsonify({"message": f"Error: {str(ex)}"}), 500
    
@app.route('/delete_student', methods=["POST"])
def delete_student():
    student_dao=StudentVo()
    data = request.get_json()  # Get the JSON data from the request
    student_id=data['student_id']
    student_dao.delete_student(student_id)
    return jsonify({
        "message":"student Deleted Successfully",
        "status":"true"
    })

@app.route('/get_student_details', methods=["POST"])
def get_student_details():
    student_dao=StudentVo()
    data = request.get_json()  # Get the JSON data from the request
    student_id=data['student_id']
    student=student_dao.find_student_by_id(student_id)
    if '_id' in student:
                    student['_id'] = str(student['_id'])
    if 'file_path' in student:  
                    student['file_path']=student['file_path'].split('base')[1]
    return jsonify({
        "message":"student details fetched Successfully",
        "student_detail":student,
        "status":"true"
    })

@app.route('/update_student', methods=["POST"])
def update_student():
    student_dao=StudentVo()
    enrollment_no = request.form.get('enrollment_no')
    _id = request.form.get('_id')
    full_name = request.form.get('full_name')
    gender = request.form.get('gender')
    age = request.form.get('age')
    file = request.files.get('face_image')
    if not file:
        student_dao.update_student(_id,{"full_name":full_name,
                                        "gender":gender,"age":age,"enrollment_no":enrollment_no})
        return jsonify({
        "message":"student details updated without changing image Successfully",
        "status":"true"
    })
       
       
    # getting previous file_path and deleting it.
   

    #Saving the new file 
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['FACE_IMAGES'],filename)
    file.save(filepath)

    # Load the image using OpenCV
    image = cv2.imread(filepath)
    
    # Load the image using OpenCV
    
    if image is None:
        try:
             os.remove(filepath)
        except Exception :
            print("Failed to remove the file")
        return jsonify({"message": "Could not read image"}), 400

    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Check if faces are detected
        if not results.detections:
            try:
                 os.remove(filepath)
            except Exception :
                print("Failed to remove the file")
            return jsonify({"message": "No faces detected"}), 400

        # Annotate the image with detected faces
        annotated_image = image.copy()
        for detection in results.detections:
            print('Nose tip:')
            print(mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
            mp_drawing.draw_detection(annotated_image, detection)
        previous_file_path=student_dao.find_student_by_id(_id)['file_path']
        try:
             os.remove(previous_file_path)        
        except Exception:
             print("Failed to remove the previous image.")
        student_dao.update_student(_id,{"full_name":full_name,
                                        "gender":gender,"age":age,"enrollment_no":enrollment_no,"file_path":filepath})
        return jsonify({
        "message":"student details updated with image changed Successfully",
        "status":"true"
    })
 
    



    
