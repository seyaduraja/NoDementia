import streamlit as st
import os
from PIL import Image
from main import load_faces, load_descriptions, save_descriptions


FACE_DIR = "faces"
DESC_FILE = "descriptions.json" 

def show_face_management():

    st.subheader("Face Profile Management")


    st.write("### Identity References")
    face_files = os.listdir(FACE_DIR)
    for file in face_files:
        st.write(f"- {file}")

    st.write("### Add New Face")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.save(os.path.join(FACE_DIR, uploaded_file.name))
        st.success(f"Saved {uploaded_file.name}")
        known_face_encodings, known_face_names = load_faces()


    st.write("### Add Face Description")
    name_input = st.text_input("Enter face name (no extension)").strip().lower()
    en_desc = st.text_area("Enter English description")
    ta_desc = st.text_area("தமிழில் விளக்கம் (Tamil Description)")

    if st.button("Save Description"):
        if name_input:
            st.session_state["face_intros"] = load_descriptions()
            st.session_state["face_intros"][name_input] = {"en": en_desc.strip(), "ta": ta_desc.strip()}
            save_descriptions(st.session_state["face_intros"])
            st.success(f"Saved description for {name_input}")
            
        else:
            st.error("Please enter a valid name.")