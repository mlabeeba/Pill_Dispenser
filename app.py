
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from database import get_pharmacist_by_email, get_all_patient_names, get_all_patients, get_pharmacist_name_by_id, \
    get_my_patients, get_medications_by_patient, get_alerts_by_patient, get_all_alerts
from datetime import date
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16) #generate randome secret key for the session
patient_names = [name[0] for name in get_all_patient_names()]  # Get names from database
patients = get_all_patients()

@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    patient_names = [name[0] for name in get_all_patient_names()]
    my_patients = get_all_patients()  # This should probably be a function that filters patients by pharmacist or something similar

    user = get_pharmacist_by_email(session['email'])
    if user is None:
        flash('Error fetching pharmacist details.', 'danger')
        return redirect(url_for('login'))

    pharmacist_name = user.get('pharmacist_name', 'Pharmacist')
    return render_template('dashboard.html', pharmacist_name=pharmacist_name, patient_names=patient_names)


@app.route('/medications')
def medications():
    my_patients = get_my_patients(session['pharmacist_id']) if patients else []
    patient = my_patients[0] if my_patients else None
    medication_list = get_medications_by_patient(patient['patient_id']) if patient else []

    return render_template('medications.html', patient_names=my_patients, medications=medication_list)

@app.route('/get_medications/<int:patient_id>')
def get_medications(patient_id):
    medications_list = get_medications_by_patient(patient_id)
    return jsonify(medications_list)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/alerts')
def alerts():
    if 'email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    # Assuming you have a function to get all patients assigned to a pharmacist
    # Modify according to your actual function and data structure
    my_patients = get_all_patients()  # This function should return all relevant patient data
    selected_patient_id = request.args.get('patient_id', type=int)

    alerts_data = []
    if selected_patient_id:
        alerts_data = get_alerts_by_patient(selected_patient_id)

    # Format alerts data if needed
    for alert in alerts_data:
        alert['date'] = alert['date'].strftime("%Y-%m-%d") if isinstance(alert['date'], date) else alert['date']

    my_patients = get_my_patients(session['pharmacist_id']) if patients else []
    patient = my_patients[0] if my_patients else None
    alert_list = get_alerts_by_patient(patient['patient_id']) if patient else []

    return render_template('alerts.html', patient_names=my_patients, alerts=alert_list)


@app.route('/get_alerts/<int:patient_id>')
def get_alerts(patient_id):
    alert_list = get_alerts_by_patient(patient_id)
    return jsonify(alert_list)

@app.route('/managepatients')
def managepatients():
    patients = get_all_patients()
    return render_template('manage-patients.html', patients=patients)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_pharmacist_by_email(email)
        if user is None:
            flash('Invalid email. Please try again.', 'danger')
            return render_template('login.html')
        elif user['password'] != password:
            flash('Invalid password. Please try again.', 'danger')
            return render_template('login.html')
        else:
            session['email'] = email  # Store pharmacist's email in the session
            session['pharmacist_id'] = user['pharmacist_id']
            return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return render_template('logout.html')


@app.route('/searchpatients')
def searchpatients():
    search_term = request.args.get('search', '').lower()

    # Fetch all patients
    all_patients = get_all_patients()

    # Filter patients based on search term
    filtered_patients = [
        p for p in all_patients
        if search_term in p['patient_name'].lower()
    ]

    # Return the filtered list as JSON
    return jsonify(filtered_patients)

def format_datetime(value, format="%Y-%m-%d"):
    """Format a datetime to a string in the specified format."""
    if value is None:
        return ""
    try:
        parsed_date = date.strptime(value, "%Y-%m-%dT%H:%M:%S")
        return parsed_date.strftime(format)
    except ValueError:
        return "Invalid date format"

app.jinja_env.filters['datetime'] = format_datetime




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
