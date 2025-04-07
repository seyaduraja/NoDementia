import streamlit as st
from main import recognize_faces 


def show_face_recognition():

# Language selection
    st.sidebar.markdown("### 🌐 Language Preference for speech")
    language = st.sidebar.radio("Select Language:", ["English", "தமிழ்"])

    lang_code = "en" if language == "English" else "ta"


    st.subheader("Face Recognition")
    if st.button("Recognize"):
        recognize_faces(lang_code)