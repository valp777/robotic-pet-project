# not using this file right now
import cv2
from deepface import DeepFace

def detecting_face_emotions(frame, cascade_face):
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Convert grayscale frame to RGB format
    #rgb_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

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
