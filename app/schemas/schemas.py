from pydantic import BaseModel


# DONOR SCHEMAS

class DonorCreate(BaseModel):
    blood_type: str
    location: str
    user_id: int


class DonorUpdate(BaseModel):
    blood_type: str
    location: str


# BLOOD REQUEST SCHEMAS

class BloodRequestCreate(BaseModel):
    requested_by: str
    blood_type: str
    units: int
    date: str


class BloodRequestUpdate(BaseModel):
    requested_by: str | None = None
    blood_type: str | None = None
    units: int | None = None
    status: str | None = None
    date: str | None = None


class BloodRequestResponse(BaseModel):
    id: int
    requested_by: str
    blood_type: str
    units: int
    status: str
    date: str

    model_config = {
        "from_attributes": True
    }


# Used by the router
BloodRequestListResponse = BloodRequestResponse