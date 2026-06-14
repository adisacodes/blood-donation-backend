from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import DonorCreate, HospitalCreate, LoginRequest, UserResponse
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter()

@router.post("/signup/donor", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup_donor(user_in: DonorCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_donor = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role="donor",
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        phone_number=user_in.phone_number,
        blood_group=user_in.blood_group
    )
    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)
    return new_donor


@router.post("/signup/hospital", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup_hospital(user_in: HospitalCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_hospital = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role="hospital",
        hospital_name=user_in.hospital_name,
        license_number=user_in.license_number,
        contact_person=user_in.contact_person,
        phone_number=user_in.phone_number
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return new_hospital

@router.post("/token")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # Look up by email instead of username to match the frontend state
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
  )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }