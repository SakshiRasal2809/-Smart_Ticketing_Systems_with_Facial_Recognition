# Smart Ticketing System with Facial Recognition 🎫🧠

A Python + Flask-based smart ticketing system using real-time facial recognition. It automates entry/exit logging, calculates fare, manages wallet balances, and supports an admin dashboard for trip history — all without physical tickets.

---

## 🚀 Features

- 👤 **Facial Recognition Based Entry/Exit**
- 🗂️ **SQLite Database Integration**
- 💰 **Auto Fare Calculation**
- 📉 **Wallet Deduction System**
- 🧑‍💼 **Admin Panel to View Trip Logs**
- 🎥 Real-Time Video Feed (OpenCV)
- 📷 Face Registration Module

---

## 📂 Folder Structure

<pre> ``` Smart_Ticketing_System/ ├── App.py # Main Flask app ├── face_recognition_module.py # Face recognition logic ├── fare_calculator.py # Fare calculation logic ├── database.py # SQLite3 database logic ├── templates/ # HTML files (Jinja2) │ ├── index.html │ ├── entry.html │ ├── exit.html │ └── admin.html ├── static/ # (Optional) CSS, JS, images ├── known_faces/ # Stored images of registered users └── README.md ``` </pre>

---

## 💻 Requirements

- Python 3.8+
- OpenCV
- Flask
- face_recognition
- dlib
- numpy
- Pillow
- SQLite3 (built-in)

---

## 🔧 Installation

```bash
git clone https://github.com/SakshiRasal2809/-Smart_Ticketing_Systems_with_Facial_Recognition.git
cd Smart_Ticketing_Systems_with_Facial_Recognition

# (Optional) create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

