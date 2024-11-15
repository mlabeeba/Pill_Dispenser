import datetime
import secrets

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16) #generate randome secret key for the session
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
            session['pharmacist_id'] = user.pharmacist_id
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    pharmacist = None
    if 'pharmacist_id' in session:
        pharmacist_id = session['pharmacist_id']
        pharmacist = get_pharmacist_by_id(pharmacist_id)  # Fetch the pharmacist by ID

    pharmacist_name = pharmacist.name if pharmacist else "Unknown Pharmacist"
    return render_template('dashboard.html', pharmacist_name=pharmacist_name)

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
        patients_list = search_patients_by_name(search_term)
    else:
        patients_list = get_all_patients()

    # Check and format DOB for each patient
    for patient in patients_list:
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

    return render_template('manage-patients.html', patients=patients_list, search_term=search_term)

@app.route('/searchpatients', methods=['GET'])
def searchpatients():
    search_term = request.args.get('search', '')

    if search_term:
        patients_list = search_patients_by_name(search_term)
    else:
        patients_list = get_all_patients()

    # Convert the patient data to JSON format
    patients_data = [{
        'patient_name': patient.name,
        'age': patient.age,
        'dob': patient.dob,
        #'medications': patient.medications,
        'notes': patient.notes
    } for patient in patients_list]

    return jsonify(patients_data)

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
