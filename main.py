import os
import json
import time
import threading
import tempfile
import numpy as np
import cv2
import pygame
import streamlit as st
import face_recognition
from gtts import gTTS
from PIL import Image

# Constants
FACE_DIR = "faces"
DESC_FILE = "descriptions.json"  # JSON file to store descriptions

# Load descriptions from JSON
def load_descriptions():
    if not os.path.exists(DESC_FILE):
        return {}
    try:
        with open(DESC_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

# Save descriptions to JSON
def save_descriptions(descriptions):
    with open(DESC_FILE, "w", encoding="utf-8") as file:
        json.dump(descriptions, file, indent=4, ensure_ascii=False)

# Initialize session state for descriptions
if "face_intros" not in st.session_state:
    st.session_state["face_intros"] = load_descriptions()

# Track last spoken times for each face
last_spoken_time = {}

# Load known face encodings and names
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
                known_face_names.append(os.path.splitext(file)[0].lower())  # Store names in lowercase
    return known_face_encodings, known_face_names

# Load faces at startup
known_face_encodings, known_face_names = load_faces()

# Function to speak introduction
def speak_intro(name, language):
    global last_spoken_time
    current_time = time.time()

    # Speak only if 30 seconds have passed since the last speech for this face
    if name not in last_spoken_time or (current_time - last_spoken_time[name] > 30):
        last_spoken_time[name] = current_time  # Update last spoken time

        # Fetch face descriptions before starting the thread
        face_intros = st.session_state.get("face_intros", {})

        def speak(face_intros, name, language):
            text = face_intros.get(name, {}).get(language, f"This is {name}. No description available.")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                tts = gTTS(text=text, lang="ta" if language == "ta" else "en")
                tts.save(temp_audio.name)
                audio_file = temp_audio.name  # Store filename

            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.quit()

            time.sleep(0.5)  # Small delay to ensure file is released
            os.remove(audio_file)  # Now delete safely

        threading.Thread(target=speak, args=(face_intros, name, language), daemon=True).start()

# Function to recognize faces
def recognize_faces(language):
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True

    stframe = st.empty()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to access webcam.")
            break

        # Resize frame for faster processing
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

                    # Speak only if the face is detected for the first time or after 30 sec
                    speak_intro(name, language)

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    video_capture.release()
    cv2.destroyAllWindows()

# Streamlit UI
st.sidebar.title("NoDementia")

# Language selection
language = st.sidebar.radio("Select Language:", ["English", "தமிழ்"])
lang_code = "en" if language == "English" else "ta"

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
    known_face_encodings, known_face_names = load_faces()  # Reload faces after adding a new one

# Form to add descriptions
st.sidebar.write("### Add Face Description")
name_input = st.sidebar.text_input("Enter face name (must match image filename, no extension)").strip().lower()
en_desc = st.sidebar.text_area("Enter English description")
ta_desc = st.sidebar.text_area("தமிழில் விளக்கம் (Tamil Description)")

if st.sidebar.button("Save Description"):
    if name_input:
        # Reload latest descriptions
        st.session_state["face_intros"] = load_descriptions()

        # Update or add new entry
        st.session_state["face_intros"][name_input] = {"en": en_desc.strip(), "ta": ta_desc.strip()}
        save_descriptions(st.session_state["face_intros"])  # Save updated JSON

        st.sidebar.success(f"Saved description for {name_input}")
    else:
        st.sidebar.error("Please enter a valid name.")

st.title("NoDementia")
if st.button("Recognize"):
    recognize_faces(lang_code)
