from pydantic import BaseModel




class DonorCreate(BaseModel):
    blood_type: str
    location: str
    user_id: int




class DonorUpdate(BaseModel):
    blood_type: str
    location: str
