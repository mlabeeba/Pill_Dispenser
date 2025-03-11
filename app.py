
import secrets
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

from database import get_all_patient_names, get_my_patients, get_medications_by_patient, get_alerts_by_patient, \
    add_medication, get_pharmacist_by_email, supabase, login_by_password, create_user, add_new_patient, \
    get_schedules_by_patient

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16) #generate randome secret key for the session
patient_names = [name[0] for name in get_all_patient_names()]  # Get names from database

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    patient_names = [name[0] for name in get_all_patient_names()]
    #my_patients = get_all_patients()  # This should probably be a function that filters patients by pharmacist or something similar

    user = get_pharmacist_by_email(session['email'])
    if user is None:
        flash('Error fetching pharmacist details.', 'danger')
        return redirect(url_for('login'))

    pharmacist_name = user.get('pharmacist_name', 'Pharmacist')
    return render_template('dashboard.html', pharmacist_name=pharmacist_name, patient_names=patient_names)


@app.route('/medications', methods=['GET', 'POST'])
def medications():
    if 'email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'GET':
        my_patients = get_my_patients(session['pharmacist_id']) or []
        patient = my_patients[0] if my_patients else None
        medication_list = get_medications_by_patient(patient['patient_id']) if patient else []
        session['current_patient_id'] = patient['patient_id'] if patient else None

    if request.method == 'POST':
        med_name = request.form['medicationName']
        dosage = request.form['dosage']
        stock = request.form['stock']
        notes = request.form['notes']
        add_medication(med_name, dosage, stock, session['current_patient_id'], session['pharmacist_id'], notes)

        my_patients = get_my_patients(session['pharmacist_id'])
        medication_list = get_medications_by_patient(session['current_patient_id'])

    return render_template('medications.html', patient_names=my_patients, medications=medication_list, current_patient_id = session['current_patient_id'])

@app.route('/get_medications/<int:patient_id>')
def get_medications(patient_id):
    session['current_patient_id'] = patient_id
    medications_list = get_medications_by_patient(patient_id)
    return jsonify(medications_list)

@app.route('/schedule')
def schedule():
    if 'email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    current_patient_id = session.get('current_patient_id')
    schedules = get_schedules_by_patient(current_patient_id) if current_patient_id else []

    return render_template('schedule.html', schedules=schedules)

@app.route('/myprofile')
def myprofile():
    if 'email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    user = get_pharmacist_by_email(session['email'])
    if user is None:
        flash('Error fetching pharmacist details.', 'danger')
        return redirect(url_for('login'))

    my_patients = get_my_patients(session['pharmacist_id']) or []
    total_patients = len(my_patients)  # Count the number of patients

    pharmacist_name = user.get('pharmacist_name', 'Pharmacist')
    pharmacist_email = user.get('email', '<EMAIL>')

    return render_template('myprofile.html', pharmacist_name=pharmacist_name,
                           pharmacist_email=pharmacist_email, total_patients=total_patients)

@app.route('/alerts')
def alerts():
    if 'email' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    # Assuming you have a function to get all patients assigned to a pharmacist
    # Modify according to your actual function and data structure
    #my_patients = get_all_patients()  # This function should return all relevant patient data
    selected_patient_id = request.args.get('patient_id', type=int)

    alerts_data = []
    if selected_patient_id:
        alerts_data = get_alerts_by_patient(selected_patient_id)

    # Format alerts data if needed
    for alert in alerts_data:
        alert['date'] = alert['date'].strftime("%Y-%m-%d") if isinstance(alert['date'], date) else alert['date']

    my_patients = get_my_patients(session['pharmacist_id']) or []
    patient = my_patients[0] if my_patients else None
    alert_list = get_alerts_by_patient(patient['patient_id']) if patient else []

    return render_template('alerts.html', patient_names=my_patients, alerts=alert_list)

@app.route('/get_alerts/<int:patient_id>')
def get_alerts(patient_id):
    alert_list = get_alerts_by_patient(patient_id)
    return jsonify(alert_list)

@app.route('/managepatients')
def managepatients():
    pharmacist_id = session.get('pharmacist_id')
    if pharmacist_id:
        patients = get_my_patients(pharmacist_id) or []
    else:
        flash('You must be logged in to view this page.', 'warning')
        return redirect(url_for('login'))

    for patient in patients:
        patient_id = patient.get('patient_id')
        if patient_id:
            medications = get_medications_by_patient(patient_id)
            patient['medications'] = ', '.join([med['med_name'] for med in medications]) if medications else 'N/A'
            patient['notes'] = ', '.join([str(med['med_notes']) if med['med_notes'] is not None else '' for med in medications]) if medications else 'N/A'
        else:
            patient['medications'] = 'N/A'
            patient['notes'] = 'N/A'

    return render_template('manage-patients.html', patients=patients)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            response = login_by_password(email, password)
            if 'error' in response:
                flash(response['error']['message'], 'danger')
                return render_template('login.html')

            session['email'] = response.user.email  # Store pharmacist's email in the session
            session['pharmacist_id'] = response.user.id  # Store pharmacist's ID in the session
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(str(e), 'danger')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return render_template('login.html')

@app.route('/searchpatients')
def searchpatients():
    search_term = request.args.get('search', '').lower()
    pharmacist_id = session.get('pharmacist_id')
    all_patients = get_my_patients(pharmacist_id)  # Assuming this fetches all necessary data

    filtered_patients = [patient for patient in all_patients if search_term in patient['patient_name'].lower()]

    # Make sure to fetch and attach medications and notes to each filtered patient
    for patient in filtered_patients:
        patient_id = patient['patient_id']
        medications = get_medications_by_patient(patient_id)
        patient['medications'] = ', '.join([med['med_name'] for med in medications]) if medications else 'N/A'
        patient['notes'] = ', '.join([med['med_notes'] for med in medications]) if medications else 'N/A'

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

@app.route('/add-med')
def add_med():
    return render_template('add-med.html')


@app.route('/add-patient', methods=['GET', 'POST'])
def add_patient():
    if 'email' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        patient_name = request.form.get('patientName')
        dob = request.form.get('dob')
        pharmacist_id = session.get('pharmacist_id')

        if not all([patient_name, dob, pharmacist_id]):
            flash('All fields are required.', 'warning')
            return redirect(url_for('add_patient'))

        # Use the newly named function to avoid conflict
        response = add_new_patient(patient_name, dob, pharmacist_id)
        if 'error' in response:
            flash(f"Error adding patient: {response['error']['message']}", 'danger')
        else:
            flash('Patient added successfully!', 'success')

        return redirect(url_for('managepatients'))

    return render_template('add-patient.html')


@app.route('/update_medications', methods=['POST'])
def update_medications():
    data = request.json
    results = []
    for med in data:
        response = supabase.table('medications').update({
            'med_name': med['med_name'],
            'dosage': med['dosage'],
            'stock_levels': med['stock_levels'],
            'med_notes': med['med_notes']
        }).eq('med_id', med['med_id']).execute()

        # Check if there is an error in the response
        if 'error' in response:
            print(f"Error updating medication {med['med_id']}: {response['error']['message']}")
            results.append({'med_id': med['med_id'], 'status': 'failed', 'error': response['error']['message']})
        else:
            results.append({'med_id': med['med_id'], 'status': 'success'})

    return jsonify({'success': True, 'results': results})

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        flash(create_user(name, email, password), 'success')
        return redirect(url_for('login'))
    # If GET request or no form submission, render the account creation form
    return render_template('create-account.html')

@app.route('/schedule-med')
def add_schedule():
    if 'email' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    # Fetch all medications for the currently selected patient
    current_patient_id = session.get('current_patient_id')
    medications = get_medications_by_patient(current_patient_id) if current_patient_id else []

    return render_template('schedule-med.html', medications=medications)

@app.route('/schedule_medication', methods=['POST'])
def schedule_medication():
    if 'email' not in session:
        flash('Please log in to schedule medication.', 'warning')
        return redirect(url_for('login'))

    data = request.json
    medication_id = data.get('medication')
    date = data.get('date')
    time = data.get('time')
    current_patient_id = session.get('current_patient_id')
    pharmacist_id = session.get('pharmacist_id')

    if not all([medication_id, date, time, current_patient_id, pharmacist_id]):
        return jsonify({'success': False, 'message': 'Missing required data'}), 400

    # Save the schedule to the database
    response = supabase.table('schedules').insert({
        'med_id': medication_id,
        'patient_id': current_patient_id,
        'pharmacist_id': pharmacist_id,
        'schedule_date': date,
        'schedule_time': time
    }).execute()

    if response.get('error'):
        return jsonify({'success': False, 'message': response['error']['message']}), 500

    return jsonify({'success': True, 'message': 'Medication scheduled successfully!'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
