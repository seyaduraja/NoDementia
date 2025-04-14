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



FACE_DIR = "faces"
DESC_FILE = "descriptions.json"  


def load_descriptions():
    if not os.path.exists(DESC_FILE):
        return {}
    try:
        with open(DESC_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_descriptions(descriptions):
    with open(DESC_FILE, "w", encoding="utf-8") as file:
        json.dump(descriptions, file, indent=4, ensure_ascii=False)


if "face_intros" not in st.session_state:
    st.session_state["face_intros"] = load_descriptions()


last_spoken_time = {}
last_print_time = {}
face_detection_times = {}


def load_faces():
    known_face_encodings = []
    known_face_names = []
    for file in os.listdir(FACE_DIR):
        if file.endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(FACE_DIR, file)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(file)[0].lower())
    return known_face_encodings, known_face_names


known_face_encodings, known_face_names = load_faces()


def speak_intro(name, language):
    global last_spoken_time
    current_time = time.time()
    if name not in last_spoken_time or (current_time - last_spoken_time[name] > 30):
        last_spoken_time[name] = current_time
        face_intros = st.session_state.get("face_intros", {})

        def speak(face_intros, name, language):
            text = face_intros.get(name, {}).get(language, f"This is {name}. No description available.")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                tts = gTTS(text=text, lang="ta" if language == "ta" else "en")
                tts.save(temp_audio.name)
                audio_file = temp_audio.name

            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.quit()
            time.sleep(0.5)
            os.remove(audio_file)

        threading.Thread(target=speak, args=(face_intros, name, language), daemon=True).start()


def recognize_faces(language):
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    stframe = st.empty()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to access webcam.")
            break

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
                    current_time = time.time()
                    face_detection_times[name] = current_time
                    speak_intro(name, language)
                    if name not in last_print_time or (current_time - last_print_time[name] > 30):
                        last_print_time[name] = current_time
                        time_str = time.strftime("%H:%M:%S", time.localtime(current_time))  # FIXED LOCAL TIME
                        st.markdown(f"""
                                <div style='
                                    background-color: #e0f7fa;
                                    padding: 16px;
                                    border-radius: 12px;
                                    box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
                                    margin: 10px 0;
                                    font-size: 18px;
                                    color: #00796b;
                                '>
                                    <strong>📍 {name.capitalize()}</strong> detected at <em>{time_str}</em>
                                </div>
                                """, unsafe_allow_html=True)
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



