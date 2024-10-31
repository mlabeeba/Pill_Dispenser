#imports
from sqlalchemy import MetaData, create_engine, Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

metadata = MetaData()
engine = create_engine('postgresql://nasyajames:Gymnast189@localhost:5432/pill_dispenser')
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

print(get_user_by_username('admin').email)

