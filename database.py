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
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    role = Column(Enum('pharmacist', 'patient', 'admin', name='role'))
    created_at = Column(DateTime, default=func.now)

def get_user_by_username(username):
    return db_session.query(Users).filter(Users.username == username).first()

def get_user_by_email(email):
    return db_session.query(Users).filter(Users.email == email).first()

#Medications table
class Medications(Base):
    __tablename__ = 'medications'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    dose = Column(Integer)
    created_at = Column(DateTime, default=func.now)


#Schedule table
class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    medication_id = Column(Integer, ForeignKey('medications.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    time = Column(DateTime)
    created_at = Column(DateTime, default=func.now)

#Logs table
class Logs(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('schedule.id'))
    acknowledged_at = Column(DateTime)
    status = Column(Enum('taken', 'missed', 'skipped', name='log_status'))

#Alerts table
class Alerts(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('schedule.id'))
    message = Column(String(100))
    alert_time = Column(DateTime)
    status = Column(Enum('pending', 'sent', 'acknowledged', name='alert_status'))
    created_at = Column(DateTime, default=func.now)
