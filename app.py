from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        return redirect(url_for('dashboard'))
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
