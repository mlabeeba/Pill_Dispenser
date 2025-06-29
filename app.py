
import secrets
from datetime import date, datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session

from database import *

app = Flask(__name__)
#app.config['SECRET_KEY'] = secrets.token_hex(16) #generate randome secret key for the session
app.config['SECRET_KEY'] = 'NMK01' #test for hardware use

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

    my_patients = get_my_patients(session['pharmacist_id']) or []
    total_patients = len(my_patients)  # Count the number of patients

    pharmacist_name = user.get('pharmacist_name', 'Pharmacist')
    return render_template('dashboard.html', pharmacist_name=pharmacist_name, patient_names=patient_names, total_patients=total_patients)


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
        notes = request.form['notes']
        add_medication(med_name, dosage, session['current_patient_id'], session['pharmacist_id'], notes)

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

    my_patients = get_my_patients(session['pharmacist_id']) or []
    patient = my_patients[0] if my_patients else None
    schedule_list = get_schedules_by_patient(patient['patient_id']) if patient else []
    session['current_patient_id'] = patient['patient_id'] if patient else None

    return render_template('schedule.html',
                           patient_names=my_patients,
                           schedules=schedule_list,
                           current_patient_id=session['current_patient_id'])



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

    my_patients = get_my_patients(session['pharmacist_id']) or []
    patient = my_patients[0] if my_patients else None
    alert_list = get_alerts_by_patient(patient['patient_id']) if patient else []

    for alert in alert_list:
        timestamp = datetime.fromisoformat(alert['timestamp'].replace("Z", "+00:00"))
        formatted_time = timestamp.strftime('%Y-%m-%d %I:%M %p')
        alert['timestamp'] = formatted_time

    return render_template('alerts.html', patient_names=my_patients, alerts=alert_list)

@app.route('/get_alerts/<int:patient_id>')
def get_alerts(patient_id):
    alert_list = get_alerts_by_patient(patient_id)

    for alert in alert_list:
        timestamp = datetime.fromisoformat(alert['timestamp'].replace("Z", "+00:00"))
        formatted_time = timestamp.strftime('%Y-%m-%d %I:%M %p')
        alert['timestamp'] = formatted_time

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
            'med_notes': med['med_notes']
        }).eq('med_id', med['med_id']).execute()

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
        return jsonify({'success': False, 'message': 'Please log in to schedule medication!'}), 403

    try:
        start_date = request.form.get('scheduleStartDate')
        end_date = request.form.get('scheduleEndDate')
        schedule_time = request.form.get('scheduleTime') or None
        interval_value = request.form.get('intervalValue') or None
        interval_unit = request.form.get('intervalUnit') or None
        med_id = request.form.get('medication')  # ✅ NEW
        patient_id = session.get('current_patient_id')
        pharmacist_id = session.get('pharmacist_id')
        dose = request.form.get('doseNumber')

        if not all([start_date, end_date, patient_id, pharmacist_id, med_id]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        data_to_insert = {
            'patient_id': int(patient_id),
            'pharmacist_id': pharmacist_id,
            'start_date': start_date,
            'end_date': end_date,
            'med_id': int(med_id),  # ✅ Include med_id
            'dose': dose
        }

        if schedule_time:
            data_to_insert['schedule_time'] = schedule_time

        if interval_value and interval_unit:
            data_to_insert['interval_value'] = int(interval_value)
            data_to_insert['interval_unit'] = interval_unit

        response = supabase.table('schedule').insert(data_to_insert).execute()

        if 'error' in response:
            print("Supabase Insert Error:", response['error'])
            return jsonify({'success': False, 'message': response['error']['message']}), 500

        return jsonify({'success': True, 'message': 'Medication scheduled successfully!'})

    except Exception as e:
        print("Unexpected Error:", str(e))
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500



@app.route('/get_schedules/<int:patient_id>')
def get_schedules(patient_id):
    session['current_patient_id'] = patient_id
    schedule_list = get_schedules_by_patient(patient_id)
    return jsonify(schedule_list)


@app.errorhandler(APIError)
def handle_supabase_errors(error):
    if "JWT expired" in str(error):
        print("⚠️ JWT expired – redirecting to login.")
        session.clear()
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for("login"))

    # Otherwise, let Flask handle it like a regular 500 error
    return str(error), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
