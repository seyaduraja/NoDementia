import streamlit as st
import os
from PIL import Image
from main import load_faces, load_descriptions, save_descriptions

FACE_DIR = "faces"
DESC_FILE = "descriptions.json"

def show_face_management():
    st.markdown("""
        <style>
            .section {
                background-color: #f9f9f9;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                margin-bottom: 30px;
            }
            .section h4 {
                color: #4B8BBE;
                margin-bottom: 20px;
            }
            .desc-label {
                font-weight: 600;
                margin-top: 15px;
            }
            .custom-input input, .custom-input textarea {
                background-color: #f0f2f6;
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 15px;
                width: 100%;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='color: #333;'>🧑‍💻 Face Profile Management</h2>", unsafe_allow_html=True)

    
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<h4>📁 Identity References</h4>", unsafe_allow_html=True)
    
    face_files = os.listdir(FACE_DIR)
    if face_files:
        st.markdown("<ul>", unsafe_allow_html=True)
        for file in face_files:
            st.markdown(f"<li>{file}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
    else:
        st.info("No faces found in the directory.")
    st.markdown("</div>", unsafe_allow_html=True)

    
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<h4>📤 Add New Face</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.save(os.path.join(FACE_DIR, uploaded_file.name))
        st.image(image, caption="Uploaded Image", width=200)
        st.success(f"Saved {uploaded_file.name}")
        known_face_encodings, known_face_names = load_faces()
    st.markdown("</div>", unsafe_allow_html=True)

    
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<h4>📝 Add Face Description</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-input">', unsafe_allow_html=True)
    name_input = st.text_input("Enter face name (without extension)").strip().lower()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-input">', unsafe_allow_html=True)
    en_desc = st.text_area("English Description")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-input">', unsafe_allow_html=True)
    ta_desc = st.text_area("தமிழில் விளக்கம் (Tamil Description)")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 Save Description", use_container_width=True):
        if name_input:
            st.session_state["face_intros"] = load_descriptions()
            st.session_state["face_intros"][name_input] = {"en": en_desc.strip(), "ta": ta_desc.strip()}
            save_descriptions(st.session_state["face_intros"])
            st.success(f"Saved description for {name_input}")
        else:
            st.error("Please enter a valid name.")
    
    st.markdown("</div>", unsafe_allow_html=True)
