from pydantic import BaseModel, EmailStr
from typing import Optional

# Base validation logic
class UserBase(BaseModel):
    email: EmailStr

# Schema for Donor Registration
class DonorCreate(UserBase):
    first_name: str
    last_name: str
    phone_number: str
    blood_group: str
    password: str

# Schema for Hospital Registration
class HospitalCreate(UserBase):
    hospital_name: str
    license_number: str
    contact_person: str
    phone_number: str
    password: str

# Schema for Login requests (Matching your frontend Login form)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Database response layout (hiding sensitive data)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
