from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="donor")

class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blood_type = Column(String, nullable=False)
    location = Column(String, nullable=False)

class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    requested_by = Column(String, nullable=False)
    blood_type = Column(String, nullable=False)
    units = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    date = Column(String, nullable=False)
