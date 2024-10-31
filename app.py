from flask import Flask, render_template, request, redirect, url_for

from database import get_user_by_email

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        email = request.form['email']
        password = request.form['password']

        #check for valid use
        user = get_user_by_email(email)
        if user is None:
            #implement flash message? and error pop up
            print('Invalid email')
            return redirect(url_for('login'))
        if user.password == password:
            return redirect(url_for('dashboard'))
        else:
            #implement flash message? and error pop up
            print('Invalid password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    pharmacist_name = "Pharmacist 1"
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
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
