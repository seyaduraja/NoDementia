import streamlit as st
from main import recognize_faces


def show_face_recognition():
    
    st.markdown("""
        <style>
            .section {
                background-color: #f9f9f9;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                margin-top: 20px;
            }
            .section h2 {
                color: #4B8BBE;
                font-family: 'Segoe UI', sans-serif;
                margin-bottom: 20px;
            }
            .custom-radio .stRadio > div {
                background-color: #ffffff;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            }
            .recognize-button button {
                background-color: #4B8BBE;
                color: white;
                font-size: 18px;
                font-weight: 600;
                padding: 0.6em 1.5em;
                border-radius: 8px;
                border: none;
                box-shadow: 0 4px 10px rgba(75, 139, 190, 0.3);
                transition: background 0.3s;
            }
            .recognize-button button:hover {
                background-color: #376a96;
            }
        </style>
    """, unsafe_allow_html=True)

    
    st.sidebar.markdown("### 🌐 Language Preference for Speech")
    with st.sidebar:
        st.markdown('<div class="custom-radio">', unsafe_allow_html=True)
        language = st.radio("Select Language:", ["English", "தமிழ்"])
        st.markdown("</div>", unsafe_allow_html=True)

    lang_code = "en" if language == "English" else "ta"

    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("<h2>📸 Face Recognition</h2>", unsafe_allow_html=True)

    st.markdown('<div class="recognize-button">', unsafe_allow_html=True)
    if st.button("🔍 Recognize"):
        recognize_faces(lang_code)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
