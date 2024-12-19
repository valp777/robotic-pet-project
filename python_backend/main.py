import cv2
#from emotion_detection.face_detection import detecting_face_emotions
from flask import Flask, jsonify
from deepface import DeepFace
import speech_recognition as sr
import requests
from dotenv import load_dotenv
import os

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

load_dotenv()

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CEREBRAS_API_URL = "https://api.cerebras.ai/v1"

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

def possible_commands(text):
    commands = ['sit', 'sleep', 'paw', 'stand', 'rollover']
    for command in commands:
        if command in text.lower():
            print(f"Command detected: {command}")
            return command
    return None

def speech_2_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text

        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
            return None
        except sr.RequestError:
            print("Error connecting to Google Speech Recognition.")
            return None

def send_2_cerebras(text):
    headers = {
        "Authorization": f"Bearer {CEREBRAS_API_KEY}",
        "Content-Type": "application/json"
    }
    message = {"user_input": text}

    try:
        response = requests.post(CEREBRAS_API_URL, json=message, headers=headers)
        if response.status_code == 200:
            reply = response.json().get("response", "")
            print(f"Cerebras Response: {reply}")
            return reply
        else:
            print("Error from Cerebras API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error communicating with Cerebras API: {e}")
        return None

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

@flaskapp.route('/talking_2_pet', methods=['POST']) # or POST??
def talking_2_pet():
    userinput = speech_2_text()
    if userinput is None:
        return jsonify({"error": "Couldn't recognize speech"}), 500

    command = possible_commands(userinput)

    if command:
        print(f"Command detected: {command}")

        return jsonify({"user_text": userinput, "movement": command})

    else:
        # send user speech text to Cerebras and get response
        chatbot_response = send_2_cerebras(userinput)
        if chatbot_response is None:
            return jsonify({"error": "Failed to get response from Cerebras API"}), 500

        return jsonify({"user_text": userinput, "chatbot_response": chatbot_response})

if __name__ == "__main__":
    try:
        start_cam()
        flaskapp.run(port=5000, debug=True)

    except KeyboardInterrupt:   # pressing Ctrl+C
        print("Stopping program")

    finally:
        release_cam(webcam)
        