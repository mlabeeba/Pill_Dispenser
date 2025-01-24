from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()  # Load environment variables from .env file

# Supabase Configuration
supabase_url = 'https://exavfgktkvnuywmxxyib.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV4YXZmZ2t0a3ZudXl3bXh4eWliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ3Njc3MzMsImV4cCI6MjA1MDM0MzczM30.Jo7wk4P-EMzGsy2n1TAb4PNuX7QGp3uS-YIDOj_4xBo'  # Replace with your Supabase secret key
supabase: Client = create_client(supabase_url, supabase_key)

# # Fetch all patients
def get_all_patients():
    response = supabase.table('patients') \
        .select('patient_name, age, dob, medications(med_name, med_notes)') \
        .execute()

    # Process data to flatten structure
    patients = []
    for patient in response.data:
        medications = patient.get('medications', [])
        med_names = ', '.join([med['med_name'] for med in medications]) if medications else 'N/A'
        med_notes = ', '.join([med['med_notes'] for med in medications]) if medications else 'N/A'

        patients.append({
            'patient_name': patient['patient_name'],
            'age': patient['age'],
            'dob': patient['dob'],
            'medications': med_names,
            'notes': med_notes
        })
    return patients


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


def get_pharmacist_name_by_id(pharmacist_id):
    # Query the Pharmacist table
    response = supabase.table('pharmacist').select('pharmacist_name').eq('pharmacist_id', pharmacist_id).execute()

    # Check if data exists
    if response.data and len(response.data) > 0:
        return response.data[0]['pharmacist_name']  # Extract the name
    return None  # Return None if no result


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
