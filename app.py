from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import get_pharmacist_by_email, get_all_patient_names, get_all_patients, get_pharmacist_name_by_id
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'labeeba'  # Replace with a secure secret key
patient_names = [name[0] for name in get_all_patient_names()]  # Get names from database
patients = get_all_patients()

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    pharmacist_name = 'Pharmacist 1'
    patient_names = [p['patient_name'] for p in get_all_patients()]  # Use correct dictionary key
    return render_template('dashboard.html', pharmacist_name=pharmacist_name, patient_names=patient_names)

@app.route('/medications')
def medications():
    patient_names = [p['patient_name'] for p in get_all_patients()]  # Use correct dictionary key
    return render_template('medications.html', patient_names=patient_names)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

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
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
