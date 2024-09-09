from bson import ObjectId
from base import app
from flask import jsonify,redirect,request
from base.com.service.live_face_recognition import live_facial_recognition
from base.com.vo.attendence_vo import AttendenceVo
from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO


@app.route('/markAttendence',methods=["POST"])
def markAttendence():
  attendence_dao=AttendenceVo()
  data = request.get_json()  
  attendence_dao.update_student(data['attendence_id'],{"status":data['status']})
  response_data = {
        "message": "success",
    }  
  return jsonify(response_data), 200

@app.route('/receiveFrames',methods=["POST"])
def receiveFrames():
    # try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract the base64-encoded image string from the data
        image_data = data['image']

        # Decode the base64 string to get binary image data
        image_data = image_data.split(",")[1]  # Split if data URL contains metadata
        image_data = base64.b64decode(image_data)

        # Convert binary data to an image using PIL
        image = Image.open(BytesIO(image_data))

        # Save the image or process it further (e.g., run facial recognition)
        image.save("received_image.png")  # Saving the image locally for debugging
        live_facial_recognition(image)
        # Perform further processing here (e.g., facial recognition)
        
        return jsonify({"message": "Image received and processed"}), 200
    # except Exception as e:
        # return jsonify({"error": str(e)}), 500