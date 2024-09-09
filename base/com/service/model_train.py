# import os
# from imutils import paths
# import face_recognition
# import pickle
# import cv2
# import os

# from base.com.vo.student_vo import StudentVo

# # our images are located in the dataset folder



# def train_model(imagePaths,student_id_list):

#   # imagePaths=["C:/Users/MAHARSHI_PATEL/Desktop/Akshar_FaceRecoginition/face-recognition-flask/base/static/face_images/vinay_t.jpg"]
#   print("[INFO] start processing faces...")
#   print(student_id_list)

#   # initialize the list of known encodings and known names
#   knownEncodings = []
#   knownNames = []
#   student_dao=StudentVo()

#   # loop over the image paths
#     # Extract the person name from the image path
#   for i, imagePath in enumerate(imagePaths):
#     print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
#     # Extract the name from the image path
#     student_vo=student_dao.find_student_by_id(student_id_list[i])
#     name = student_vo['full_name']
#     print("name >>>>>>>>>>>>>>>>",name)

#     # load the input image and convert it from RGB (OpenCV ordering)
#     # to dlib ordering (RGB)
#     abs_path = os.path.abspath(imagePath)
#     print(f"Absolute path: {abs_path}")
#     image = cv2.imread(abs_path)
#     print(abs_path)  
#     if image is None:
#       print(f"Error: Unable to load image at {abs_path}")
#     else:
#       rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # detect the (x, y)-coordinates of the bounding boxes
#     # corresponding to each face in the input image
#       boxes = face_recognition.face_locations(rgb,
#         model="hog")

#       # compute the facial embedding for the face
#       encodings = face_recognition.face_encodings(rgb, boxes)

#       # loop over the encodings
#       for encoding in encodings:
#         # add each encoding + name to our set of known names and
#         # encodings
#         knownEncodings.append(encoding)
#         knownNames.append(name)

#     # dump the facial encodings + names to disk
#     print("[INFO] serializing encodings...")
#     file_path = os.path.abspath("encodings.pickle")
#     print(f"[INFO] Encodings will be saved at: {file_path}")
#     data = {"encodings": knownEncodings, "names": knownNames}
#     f = open(file_path, "wb")
#     f.write(pickle.dumps(data))
#     f.close()
      
import os
import pickle
import face_recognition
import cv2
from base.com.vo.student_vo import StudentVo

def load_existing_encodings(file_path):
    """Load existing encodings from the file if it exists."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
    return {"encodings": [], "names": []}

def save_encodings(file_path, knownEncodings, knownNames):
    """Save encodings and names to the file."""
    existing_data = load_existing_encodings(file_path)
    
    # Append new data to the existing data
    existing_data["encodings"].extend(knownEncodings)
    existing_data["names"].extend(knownNames)
    
    # Serialize and write the updated data to the file
    with open(file_path, "wb") as f:
        pickle.dump(existing_data, f)

def train_model(imagePaths, student_id_list):
    print("[INFO] start processing faces...")
    print(student_id_list)

    # Initialize the list of known encodings and names
    knownEncodings = []
    knownNames = []
    student_dao = StudentVo()

    # Loop over the image paths
    for i, imagePath in enumerate(imagePaths):
        print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
        
        # Extract the name from the image path
        
        name = student_id_list[i]
        print("name >>>>>>>>>>>>>>>>", name)

        # Load the input image and convert it from RGB (OpenCV ordering) to dlib ordering (RGB)
        abs_path = os.path.abspath(imagePath)
        print(f"Absolute path: {abs_path}")
        image = cv2.imread(abs_path)
        if image is None:
            print(f"Error: Unable to load image at {abs_path}")
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

