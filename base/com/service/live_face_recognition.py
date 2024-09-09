# import face_recognition
# import pickle
# import cv2
# import numpy as np
# from PIL import Image



# def live_facial_recognition(image):
  
#   # initialize 'currentname' to trigger only when a new person is identified
#   currentname = "unknown"
#   # determine faces from encodings.pickle file model created from train_model.py
#   encodingsP = "encodings.pickle"
#   # use this xml file
#   cascade = "C:/Users/MAHARSHI_PATEL/Desktop/Akshar_FaceRecoginition/face-recognition-flask/base/com/service/haarcascade_frontalface_default.xml"
#   print("[INFO] loading encodings + face detector...")
#   data = pickle.loads(open(encodingsP, "rb").read())
#   detector = cv2.CascadeClassifier(cascade)

#   # initialize the video stream and allow the camera sensor to warm up
#   if image is None:
#     print(f"Error: Unable to load image at image not found ")
#     return
#   rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # detect the (x, y)-coordinates of the bounding boxes
#     # corresponding to each face in the input image
#   boxes = face_recognition.face_locations(rgb,
#         model="hog")

#       # compute the facial embedding for the face
#   encodings = face_recognition.face_encodings(rgb, boxes)
#   names = []

#     # loop over the facial embeddings
#   for encoding in encodings:
#     # attempt to match each face in the input image to our known
#     # encodings
#     matches = face_recognition.compare_faces(data["encodings"],
#       encoding)
#     name = "Maharshi Patel" # if face is not recognized, then print Unknown

#     # check to see if we have found a match
#     if True in matches:
#       # find the indexes of all matched faces then initialize a
#       # dictionary to count the total number of times each face
#       # was matched
#       matchedIdxs = [i for (i, b) in enumerate(matches) if b]
#       counts = {}

#       # loop over the matched indexes and maintain a count for
#       # each recognized face
#       for i in matchedIdxs:
#         name = data["names"][i]
#         counts[name] = counts.get(name, 0) + 1

#       # determine the recognized face with the largest number
#       # of votes (note: in the event of an unlikely tie Python
#       # will select first entry in the dictionary)
#       name = max(counts, key=counts.get)
      
#       # if someone in your dataset is identified, print their name on the screen
#       if currentname != name:
#         currentname = name
#         print(currentname)
    
#     # update the list of names
#     names.append(name)

#     # loop over the recognized faces
   

#     # display the image to our screen
   
#     # quit when 'q' key is pressed
   

#     # update the FPS counter
   

#   # stop the timer and display FPS information
  
import os
import face_recognition
import pickle
import cv2
import numpy as np

def live_facial_recognition(image):
    # Initialize 'currentname' to trigger only when a new person is identified
    currentname = "unknown"
    # Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings.pickle"
    # Use this xml file
    cascade = "C:/Users/MAHARSHI_PATEL/Desktop/Akshar_FaceRecoginition/face-recognition-flask/base/com/service/haarcascade_frontalface_default.xml"
    
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())
    detector = cv2.CascadeClassifier(cascade)
    image = cv2.imread("received_image.png")
    # Initialize the video stream and allow the camera sensor to warm up
    if image is None:
        print(f"Error: Unable to load image at image not found ")
        return  # Exit the function if the image is None
    
    # Convert the image from BGR to RGB format (since OpenCV loads images in BGR format)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb, model="hog")

    # Compute the facial embedding for the faces
    encodings = face_recognition.face_encodings(rgb, boxes)
    
    # names = []

    # Loop over the facial embeddings
    for encoding in encodings:
        # Attempt to match each face in the input image to our known encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        # name = "Maharshi Patel"  # Default to "Maharshi Patel" if face is not recognized

        # Check to see if we have found a match
        if True in matches:
            # Find the indexes of all matched faces and initialize a dictionary to count the total number of times each face was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # Loop over the matched indexes and maintain a count for each recognized face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # Determine the recognized face with the largest number of votes
            name = max(counts, key=counts.get)
            
            # If someone in your dataset is identified, print their name on the screen
            if currentname != name:
                currentname = name
                print(currentname)
        
        # Update the list of names
        # names.append(name)

    # # Loop over the recognized faces
    # for ((top, right, bottom, left), name) in zip(boxes, names):
    #     # Draw the predicted face name on the image
    #     cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    #     cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    
    os.remove("received_image.png")
    