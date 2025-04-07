import streamlit as st
from FaceManagement import show_face_management  
from FaceRecognition import show_face_recognition

# Dummy credentials (use a secure method like hashed passwords for production)
USERNAME = "admin"
PASSWORD = "1234"

st.set_page_config(page_title="NoDementia", page_icon="")

def login():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username == USERNAME and password == PASSWORD:
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        st.sidebar.title("Navigation")
        choice = st.sidebar.selectbox("Go to", [ "Face Recognition", "Face Management"])

        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()

        if choice == "Face Recognition":
           show_face_recognition()
        elif choice == "Face Management":
            show_face_management()
      
    else:
        login()

if __name__ == "__main__":
    main()
