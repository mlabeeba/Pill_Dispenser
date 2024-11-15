#imports
from sqlalchemy import MetaData, create_engine, Column, Integer, String, Enum, DateTime, func, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")

metadata = MetaData()
engine = create_engine(f"postgresql://{db_user}:{db_password}@localhost:5432/{db_name}")
Base = declarative_base()
db_session = sessionmaker(bind=engine)()

#Users table
class Pharmacists(Base):
    __tablename__ = 'pharmacists'
    pharmacist_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))

def get_user_by_email(email):
    return db_session.query(Pharmacists).filter(Pharmacists.email == email).first()

def get_pharmacist_by_id(pharmacist_id):
    return db_session.query(Pharmacists).get(pharmacist_id)

#Patients table
class Patients(Base):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True)
    pharmacist_id = Column(Integer, ForeignKey('pharmacists.pharmacist_id'))
    name = Column(String(100))
    dob = Column(DateTime)
    age = Column(Integer)


#Medications table
class Medications(Base):
    __tablename__ = 'medications'
    medication_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.patient_id'))
    name = Column(String(100))
    stock_level = Column(Integer)
    notes = Column(String(100))
    dose = Column(Integer)

def get_medications_by_patient_id(patient_id):
    return db_session.query(Medications).filter(Medications.patient_id == patient_id).all()


#Schedule table
class Schedule(Base):
    __tablename__ = 'schedules'
    schedule_id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

#Alerts table
class Alerts(Base):
    __tablename__ = 'alerts'
    alert_id = Column(Integer, primary_key=True)
    pharmacist_id = Column(Integer, ForeignKey('pharmacists.pharmacist_id'))
    date = Column(DateTime)
    status = Column(Enum('pending', 'triggered', 'acknowledged', name='alert_status'))
    notes = Column(String(100))
