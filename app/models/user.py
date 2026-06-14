from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "donor" or "hospital"
    
    # --- Donor Specific Fields ---
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)

    # --- Hospital Specific Fields ---
    hospital_name = Column(String, nullable=True)
    license_number = Column(String, nullable=True)
    contact_person = Column(String, nullable=True)