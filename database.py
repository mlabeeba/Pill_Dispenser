from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, func, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from supabase import create_client, Client

# Supabase Configuration
supabase_url = 'https://exavfgktkvnuywmxxyib.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV4YXZmZ2t0a3ZudXl3bXh4eWliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ3Njc3MzMsImV4cCI6MjA1MDM0MzczM30.Jo7wk4P-EMzGsy2n1TAb4PNuX7QGp3uS-YIDOj_4xBo'  # Replace with your Supabase secret key
supabase: Client = create_client(supabase_url, supabase_key)

# Fetch all patients
def get_all_patients():
    response = supabase.table('patients').select("*").execute()
    return response.data

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
