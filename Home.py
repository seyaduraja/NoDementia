import streamlit as st
from FaceManagement import show_face_management  
from FaceRecognition import show_face_recognition

USERNAME = "admin"
PASSWORD = "1234"

st.set_page_config(page_title="NoDementia", page_icon="🧠")

# Header
def header():
    st.markdown("""
        <style>
            .header {
                background-color: #4B8BBE;
                padding: 20px 10px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
            }
            .header h1 {
                color: white;
                font-family: 'Segoe UI', sans-serif;
                margin: 0;
            }
            /* Custom input style */
            .custom-input input {
                background-color: #f0f2f6;
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #ccc;
                box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.05);
                font-size: 16px;
            }
        </style>
        <div class="header">
            <h1> NoDementia</h1>
        </div>
    """, unsafe_allow_html=True)

# Login screen
def login():
    header()
    st.subheader("🔐 Login")

    with st.container():
        st.markdown('<div class="custom-input">', unsafe_allow_html=True)
        username = st.text_input("Username")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="custom-input">', unsafe_allow_html=True)
        password = st.text_input("Password", type="password")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Login", use_container_width=True):
        if username == USERNAME and password == PASSWORD:
            st.session_state["logged_in"] = True
            st.success("✅ Logged in successfully!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# Main dashboard
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        header()

        # --- Sidebar Layout ---
        st.sidebar.markdown("""
            <style>
                .sidebar-section {
                    background-color: #f0f4f8;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
                }
                .sidebar-section h4 {
                    margin-top: 0;
                    font-size: 18px;
                    color: #4B8BBE;
                }
                .sidebar-section p {
                    margin: 0;
                    font-size: 14px;
                }
            </style>
            <div class="sidebar-section">
                <h4>🧑 Patient Info</h4>
                <p><strong>Name:</strong> John Doe</p>
                <p><strong>Age:</strong> 68</p>
                <p><strong>Diagnosis:</strong> Early-stage Dementia</p>
            </div>
        """, unsafe_allow_html=True)

        # --- Navigation ---
        st.sidebar.title("📁 Navigation")
        choice = st.sidebar.selectbox("Go to", ["Face Recognition", "Face Management"])

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

