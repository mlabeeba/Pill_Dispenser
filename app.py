from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import get_user_by_email, get_all_patient_names, get_all_patients, Patients, db_session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'labeeba'  # Replace with a secure secret key
patient_names = [name[0] for name in get_all_patient_names()]  # Get names from database
patients = get_all_patients()

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        email = request.form['email']
        password = request.form['password']

        # Check for valid user
        user = get_user_by_email(email)
        if user is None:
            flash('Invalid email. Please try again.', 'danger')
            return render_template('login.html')
        elif user.password != password:
            flash('Invalid password. Please try again.', 'danger')
            return render_template('login.html')
        else:
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    pharmacist_name = "Pharmacist 1"
    return render_template('dashboard.html', pharmacist_name=pharmacist_name, patient_names=patient_names)

@app.route('/medications')
def medications():
    return render_template('medications.html', patient_names=patient_names)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/managepatients', methods=['GET'])
def managepatients():
    search_term = request.args.get('search', '')

    if search_term:
        patients = db_session.query(Patients).filter(Patients.patient_name.ilike(f"%{search_term}%")).all()
    else:
        patients = db_session.query(Patients).all()

    # Check and format DOB for each patient
    for patient in patients:
        if isinstance(patient.dob, str):
            try:
                # Try to parse the string to a datetime object
                patient.dob = datetime.strptime(patient.dob, '%Y-%m-%d %H:%M:%S')  # Adjust format if needed
            except ValueError:
                # Handle the case if the format doesn't match
                pass
        if isinstance(patient.dob, datetime):
            # Format datetime object to desired string format
            patient.dob = patient.dob.strftime('%Y-%m-%d')

    return render_template('manage-patients.html', patients=patients, search_term=search_term)

@app.route('/searchpatients', methods=['GET'])
def searchpatients():
    search_term = request.args.get('search', '')

    if search_term:
        patients = db_session.query(Patients).filter(Patients.patient_name.ilike(f"%{search_term}%")).all()
    else:
        patients = db_session.query(Patients).all()

    # Convert the patient data to JSON format
    patients_data = [{
        'patient_name': patient.patient_name,
        'age': patient.age,
        'dob': patient.dob,
        'medications': patient.medications,
        'notes': patient.notes
    } for patient in patients]

    return jsonify(patients_data)

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
