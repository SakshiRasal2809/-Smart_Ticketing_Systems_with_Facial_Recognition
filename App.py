from flask import Flask, render_template, request, redirect, url_for, session
from utils.db_utils import (
    init_db, add_passenger, passenger_exists, get_all_trips,
    log_trip, update_trip_exit, get_passenger, update_wallet
)
from utils.fare_utils import calculate_fare
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for session storage

# Initialize DB tables
init_db()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/capture_photo', methods=['POST'])
def capture_photo():
    name = request.form.get('name')

    if not name:
        return "Error: Please enter a passenger name before capturing photo."

    if passenger_exists(name):
        return "Error: Passenger with this name already exists. Please choose another name."

    from utils.face_utils import capture_face
    photo_path = capture_face(name)

    if photo_path:
        # Store in session for /register
        session['photo_path'] = photo_path
        session['name_for_registration'] = name
        return redirect(url_for('register'))
    else:
        return "Error: Photo capture failed."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Pull name from form or session
        name = request.form.get('name') or session.get('name_for_registration')
        wallet = float(request.form.get('wallet', 0))
        photo_path = session.get('photo_path')

        if not name:
            return "Error: Passenger name is missing. Please capture photo first."

        if passenger_exists(name):
            return "Error: Passenger already exists."

        if not photo_path:
            return "Error: Please capture photo before registering."

        add_passenger(name, wallet, photo_path)

        # Clear stored session values
        session.pop('photo_path', None)
        session.pop('name_for_registration', None)

        return redirect(url_for('home'))

    return render_template("register.html")


@app.route('/dashboard')
def dashboard():
    trips = get_all_trips()
    return render_template("dashboard.html", trips=trips)

@app.route('/entry', methods=['GET', 'POST'])
def entry_gate():
    if request.method == 'POST':
        from utils.face_utils import recognize_face
        name = recognize_face()

        if not name:
            return "No face detected or passenger not recognized."

        passenger = get_passenger(name)
        if passenger:
            log_trip(name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return redirect(url_for('dashboard'))
        else:
            return "Passenger not registered."

    return render_template("entry_gate.html")

@app.route('/exit', methods=['GET', 'POST'])
def exit_gate():
    if request.method == 'POST':
        from utils.face_utils import recognize_face
        name = recognize_face()

        if not name:
            return "No face detected or passenger not recognized."

        passenger = get_passenger(name)
        if passenger:
            fare = calculate_fare(None, None, distance_km=5)
            new_wallet = passenger['wallet'] - fare
            if new_wallet >= 0:
                update_wallet(name, new_wallet, transaction_type="fare")
                update_trip_exit(
                    name,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    5,
                    fare
                )
            else:
                return "Insufficient balance."
        else:
            return "Passenger not registered."

        return redirect(url_for('dashboard'))

    return render_template("exit_gate.html")

if __name__ == '__main__':
    app.run(debug=True)
