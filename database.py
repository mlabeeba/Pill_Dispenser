from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # Load environment variables from .env file

# Supabase Configuration
supabase_url = 'https://exavfgktkvnuywmxxyib.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV4YXZmZ2t0a3ZudXl3bXh4eWliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ3Njc3MzMsImV4cCI6MjA1MDM0MzczM30.Jo7wk4P-EMzGsy2n1TAb4PNuX7QGp3uS-YIDOj_4xBo'  # Replace with your Supabase secret key
supabase: Client = create_client(supabase_url, supabase_key)

# Fetch patient names
def get_all_patient_names():
    response = supabase.table('patients').select("patient_name").execute()
    return [row['patient_name'] for row in response.data]

# Fetch pharmacist by email
def get_pharmacist_by_email(email):
    response = supabase.table('pharmacist').select("*").eq('email', email).execute()
    if response.data:
        return response.data[0]  # Return the first pharmacist matching the email
    return None

# Login authentication by email and password
def login_by_password(email, password):
    response = supabase.auth.sign_in_with_password({'email': email, 'password': password})
    return response;

# Fetch pharmacist specific patients
def get_my_patients(pharmacist_id):
    response = supabase.table('patients').select('*').eq('pharmacist_id', pharmacist_id).execute()
    return response.data if response.data else None


# Fetch patient medications
def get_medications_by_patient(patient_id):
    response = supabase.table('medications').select('*').eq('patient_id', patient_id).execute()
    return response.data if response.data else None


def get_alerts_by_patient(patient_id):
    response = supabase.table('alerts').select('*').eq('patient_id', patient_id).execute()
    return response.data if response.data else []


def get_all_alerts():
    response = supabase.table('alerts').select("*").order('date', desc=True).execute()
    return response.data


# add medications to database
def add_medication(med_name, dosage, stock, patient_id, pharmacist_id, med_notes=None):
    data = {
        'med_name': med_name,
        'dosage': dosage,
        'stock_levels': stock,
        'patient_id': patient_id,
        'pharmacist_id': pharmacist_id
    }
    if med_notes:
        data['med_notes'] = med_notes

    response = supabase.table('medications').insert(data).execute()
    return response

def add_new_patient(patient_name, dob, pharmacist_id):
    data = {
        'patient_name': patient_name,
        'dob': dob,
        'pharmacist_id': pharmacist_id
    }
    response = supabase.table('patients').insert(data).execute()
    return response


# add security measures/authentication measures here too?
def create_user(name, email, password):
    # Check if user already exists in the profiles table
    existing_profile = supabase.table("pharmacist").select("UID").eq("email", email).execute()

    if existing_profile.data:
        return "Email already registered, please login or reset password."

    # Otherwise, add user to authentication table
    try:
        data = supabase.auth.sign_up({
            'email': email,
            'password': password,
            'options': {
                'email_redirect_to': 'https://localhost:5000/login',
            },
        })
        UID = data.user.id

        # if successful, add user to pharmacist table
        data = {
            'UID': UID,
            'pharmacist_name': name,
            'email': email,
        }
        supabase.table('pharmacist').insert(data).execute()

        return "Confirmation email sent! Please check your email to confirm account."
    except Exception as e:
        print("Error: ", e)
        return "Error: ", e

def check_user_exists(email):
    # Function to check if user already exists in the database
    # This is a placeholder function
    pass


def get_schedules_by_patient(patient_id):
    response = supabase.table('schedule').select('*').eq('patient_id', patient_id).execute()
    return response.data if response.data else []

