# 💊 Smart Prescription Dispenser Web-Application

A full-stack web application designed to support pharmacists in scheduling and managing patients’ medications remotely. This system integrates Supabase for database/authentication, Flask for backend routing, and a dynamic HTML/CSS/JS frontend.

---

## Features

* Pharmacist account registration and login with Supabase Auth
* Patient management (add, view, search)
* Medication management (add, edit, schedule)
* Medication scheduling with popups and form validation
* Dynamic table rendering & inline editing
* Supabase as secure, scalable backend storage
* Alerts and logs based on stock levels or patient activity
* Responsive frontend with clean styling

---

## Tech Stack

* **Frontend**: HTML, CSS (`med-style.css`, `schedule-med-style.css`), JavaScript (`popup.js`)
* **Backend**: Python (Flask)
* **Database**: Supabase (PostgreSQL + Auth + Storage)
* **Authentication**: Supabase Auth
* **Templating**: Jinja2

---

## Hardware Integration

This web application was developed to work in tandem with a **custom-built smart pill dispenser** created by the hardware members of our team. Once a pharmacist schedules a medication for a patient, the dispenser automatically releases the correct dosage at the scheduled time.

The dispenser includes:

* Multiple compartments for different medications
* A stepper motor mechanism for rotating compartments
* A Raspberry Pi for executing scheduled dispense commands

**Hardware Prototype:**
<p align="center">
  <img src="static/images/dispenser_photo.jpg" alt="Smart Dispenser Hardware" width="400"/>
</p>
<p align="center"><em>Actual image of the physical dispenser made by our hardware team.</em></p>

*Hardware developed by:*

* **Harrison Kalathil**
* **Maninder Arora**

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/nasyatj/Pill_Dispenser.git
cd Pill_Dispenser
```

### 2. Set Up Environment

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root folder:

```
SUPABASE_URL=your-supabase-url  
SUPABASE_KEY=your-secret-api-key
```

### 3. Run Flask App

```bash
python app.py
```

The app will run at: `http://localhost:5000`

---

## 📁 Project Structure

```
├── app.py                 # Flask routes and logic
├── database.py            # Supabase integration for DB operations
├── templates/             # HTML templates (Jinja2)
│   ├── medications.html
│   ├── schedule-med.html
│   └── ...
├── static/
│   ├── styles.css
│   ├── med-style.css
│   ├── schedule-med-style.css
│   └── popup.js
├── images/
│   └── dispenser_photo.jpg    # Image of the hardware (placeholder)
└── .env                   # Supabase credentials (excluded from repo)
```

---

## Usage Flow

1. **Sign up or log in** as a pharmacist
2. **Add patients** to your account
3. **Manage medications** for each patient
4. **Schedule medication times** via popup form
5. **Push changes to device** (mocked in frontend)
6. **Track alerts** and low stock via `/alerts` page

---

## Security Notes

* Authentication is handled securely via Supabase.
* Environment keys are stored in `.env` and should not be committed.
* Backend endpoints validate session data before processing requests.

---

## Authors

* **Nasya James** — [@nasyatj](https://github.com/nasyatj)
* **Maria Labeeba** — [@mlabeeba](https://github.com/mlabeeba)
* **Hardware Members** — Harrison Kalathil, Maninder Arora

