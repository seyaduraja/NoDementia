# 🚀 Project Setup Guide

## 🛠️ Prerequisites
- Ensure you have **🐍 Python 3.10.10** installed.
- Install **📦 pip** and **🌐 virtualenv** if not already installed.

## 📌 Step-by-Step Installation Guide

### 1️⃣ Create a Virtual Environment
Open a 🖥️ terminal or command prompt and run:
```sh
python -m venv venv
```

### 2️⃣ Activate the Virtual Environment
- **🪟 Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **🍎 Mac/Linux:**
  ```sh
  source venv/bin/activate
  ```

### 3️⃣ Install `dlib`
Ensure the `dlib` package is installed using the provided 📂 wheel file:
```sh
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
```

### 4️⃣ Install Required Packages
Run the following command to install all dependencies 📜 from `requirements.txt`:
```sh
pip install -r requirements.txt
```

### 5️⃣ Run the 🚀 Streamlit App
Start the 📊 Streamlit application using:
```sh
streamlit run main.py
```

## 📝 Additional Notes
- If you encounter ❌ issues with `dlib`, ensure you have installed the necessary ⚙️ system dependencies.
- The `requirements.txt` file contains all the dependencies 📜 needed for the project.
- Always 🔄 activate the virtual environment before running the project.

🎉 Enjoy using the app!

