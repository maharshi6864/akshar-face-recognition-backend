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

# Read frame from video capture
    

    # Perform object detection using YOLO
    results = model(img, stream=True, verbose=False)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            # Extract confidence score and class index
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = box.cls[0]

            # Get class name based on class index
            name = classNames[int(cls)].upper()
            
            if conf > confidence:
                if name == "REAL":
                    # Draw green rectangle if real
                    color = (0, 255, 0)
                    # fl = fr.face_locations(img)
                    # face_enco = fr.face_encodings(img,fl)
                    # if face_enco:
                    #  results = fr.compare_faces([known_enco], face_enco[0])

                    #  print(results)

                    #  if results[0]: 
                    #     cv2.putText(img,'Detected',(100,100),1,1,(0,255,0),1)
                    #  else:
                    #     cv2.putText(img,'Not-Detected',(100,100),1,1,(0,0,255),1)
                else:  
                    # Draw red rectangle if fake
                    color = (0, 0, 255)
                # Draw rectangle around the object
                cvzone.cornerRect(img, (x1, y1, w, h), colorC=color, colorR=color)
                # Display class name and confidence score
                cvzone.putTextRect(img, f'{name} {int(conf*100)}%', (max(0, x1), max(35, y1)), scale=2, thickness=2, colorR=color, colorB=color)

    # Display the frame
    cv2.imshow("Image", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

# Release the video capture object
cap.release()
cv2.destroyAllWindows()