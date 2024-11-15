import secrets

from flask import Flask, render_template, request, redirect, url_for, session

from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16) #generate randome secret key for the session

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
            print('Invalid email')
            return redirect(url_for('error'))  # Redirect to error page for invalid email

        if user.password == password:
            session['pharmacist_id'] = user.pharmacist_id
            return redirect(url_for('dashboard'))
        else:
            print('Invalid password')
            return redirect(url_for('error'))  # Redirect to error page for invalid password

    return render_template('login.html')

@app.route('/login-error')
def error():
    # Render the error page
    return render_template('login-error.html')

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
    return render_template('medications.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/managepatients')
def managepatients():
    return render_template('manage-patients.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
