import cv2
#from emotion_detection.face_detection import detecting_face_emotions
from flask import Flask, jsonify
from deepface import DeepFace
import speech_recognition as sr
import requests

"""
flaskapp = Flask(__name__)

def start_cam():
    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Error: Counld not open camera")
    return webcam

def release_cam(webcam):
    # release the camera resource
    webcam.release()
    cv2.destroyAllWindows()

def main():

    webcam = start_cam()

    # load face detector 
    cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

    try:
        while True:

            # read current frame from webcam 
            ret, frame = webcam.read()
            if not ret:
                print("Error: Could not read frame")
                break

            emotion = detecting_face_emotions(frame, cascade_face)
            print(f"Detected Facial Emotion: {emotion}")

            # displaying results 
            cv2.imshow('Emotion', frame)

            # break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:   # pressing Ctrl+C
        print("Stopping program")

    finally:
        release_cam(webcam)

if __name__ == "__main__":
    main()

"""
# initializing flask app
flaskapp = Flask(__name__)

# initializing webcam
webcam = None

# load face detector 
cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

def start_cam():
    global webcam
    webcam = cv2.VideoCapture(0)
    if not webcam.isOpened():
        print("Error: Counld not open camera")
    return webcam

def release_cam(webcam):
    # release the camera resource
    webcam.release()
    cv2.destroyAllWindows()

def detecting_face_emotions(frame):
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = cascade_face.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # checking for faces 
    if len(faces) > 0:
        
        # loop through faces 
        for (x, y, w, h) in faces:
            face_region = frame[y:y + h, x:x + w]

            # emotion prediction
            result = DeepFace.analyze(face_region, actions=['emotion'])

            # dominant emotion
            emotion = max(result[0]['emotion'], key=result[0]['emotion'].get)

            # or maybe try this:
            # emotion = result[0]['emotion']
            # print(emotion)

            # draw box and label 
            label = f'Emotion: {emotion}'
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            return emotion
    else:
        return "Face not detected"

###
"""
def main():

    webcam = start_cam()

    try:
        while True:

            # read current frame from webcam 
            ret, frame = webcam.read()
            if not ret:
                print("Error: Could not read frame")
                break

            emotion = detecting_face_emotions(frame)
            print(f"Detected Facial Emotion: {emotion}")

            # displaying results 
            cv2.imshow('Emotion', frame)

            # break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:   # pressing Ctrl+C
        print("Stopping program")

    finally:
        release_cam(webcam)

if __name__ == "__main__":
    main()
"""
### old way above 

@flaskapp.route('/detected_emotion', methods=['GET'])
def detected_emotion():
    if webcam is None:
        start_cam()

    # read current frame from webcam 
    ret, frame = webcam.read()
    if not ret:
        return jsonify({"error": "Failed to capture frame"}), 500

    emotion = detecting_face_emotions(frame)
    print(f"Detected Facial Emotion: {emotion}")

    # displaying results 
    cv2.imshow('Emotion', frame)

    return jsonify({"emotion": emotion})

if __name__ == "__main__":
    try:
        start_cam()
        flaskapp.run(port=5000, debug=True)

    except KeyboardInterrupt:   # pressing Ctrl+C
        print("Stopping program")

    finally:
        release_cam(webcam)
        