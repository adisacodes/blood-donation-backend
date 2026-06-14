from pydantic import BaseModel
from typing import Optional

class BloodRequestCreate(BaseModel):
    requested_by: str
    blood_type: str
    units: int
    date: str

class BloodRequestUpdate(BaseModel):
    blood_type: Optional[str] = None
    units: Optional[int] = None
    status: Optional[str] = None
    date: Optional[str] = None

class BloodRequestResponse(BaseModel):
    id: int
    requested_by: str
    blood_type: str
    units: int
    status: str
    date: str

    class Config:
        from_attributes = True

class BloodRequestListResponse(BaseModel):
    requests: list[BloodRequestResponse]

class DonorMatchResponse(BaseModel):
    id: int
    user_id: int
    blood_type: str
    location: str

    class Config:
        from_attributes = True
