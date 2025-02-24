import streamlit as st
import face_recognition
import cv2
import numpy as np
import os
from PIL import Image

# Folder containing face images
FACE_DIR = "faces"

# Load known face encodings and their names dynamically
def load_faces():
    known_face_encodings = []
    known_face_names = []
    for file in os.listdir(FACE_DIR):
        if file.endswith(('.jpg', '.png', '.jpeg')):
            path = os.path.join(FACE_DIR, file)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(file)[0])
    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_faces()

def recognize_faces():
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    
    stframe = st.empty()
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to access webcam.")
            break

        # Resize frame to 1/4 size for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    video_capture.release()
    cv2.destroyAllWindows()

st.sidebar.title("NoDementia")
st.sidebar.write("### Faces Folder")
face_files = os.listdir(FACE_DIR)
for file in face_files:
    st.sidebar.write(f"- {file}")

st.sidebar.write("### Add New Face Image")
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image.save(os.path.join(FACE_DIR, uploaded_file.name))
    st.sidebar.success(f"Saved {uploaded_file.name}")
    known_face_encodings, known_face_names = load_faces()

st.title("NoDementia")
if st.button("Recognize"):
    recognize_faces()
