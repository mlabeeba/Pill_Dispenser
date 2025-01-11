from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from database import get_pharmacist_by_email, get_all_patient_names, get_all_patients
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a random secret key for the session
patient_names = [p['patient_name'] for p in get_all_patients()]


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    # Fetch pharmacist name from the database using email
    user = get_pharmacist_by_email(session['email'])
    if user is None:
        flash('Error fetching pharmacist details.', 'danger')
        return redirect(url_for('login'))

    pharmacist_name = user.get('pharmacist_name', 'Pharmacist')
    return render_template('dashboard.html', pharmacist_name=pharmacist_name, patient_names=patient_names)


@app.route('/medications')
def medications():
    return render_template('medications.html', patient_names=patient_names)


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/alerts')
def alerts():
    return render_template('alerts.html', patient_names=patient_names)


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
