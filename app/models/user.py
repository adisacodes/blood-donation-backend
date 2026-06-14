from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # "donor" or "hospital"
    
    # --- Donor Specific Fields ---
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    blood_group = Column(String(5), nullable=True)

    # --- Hospital Specific Fields ---
    hospital_name = Column(String(150), nullable=True)
    license_number = Column(String(100), nullable=True)
    contact_person = Column(String(100), nullable=True)