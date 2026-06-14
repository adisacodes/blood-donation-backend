from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Donor

from app.schemas.schemas import DonorCreate, DonorUpdate

router = APIRouter()


@router.post("/")
def create_donor(blood_type: str, location: str, user_id: int, db: Session = Depends(get_db)):
    donor = Donor(blood_type=blood_type, location=location, user_id=user_id)
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


@router.get("/")
def get_donors(blood_type: str = None, db: Session = Depends(get_db)):
    if blood_type:
        return db.query(Donor).filter(Donor.blood_type == blood_type).all()
    return db.query(Donor).all()


@router.put("/{donor_id}")
def update_donor(donor_id: int, blood_type: str, location: str, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    donor.blood_type = blood_type
    donor.location = location
    db.commit()
    return donor


@router.delete("/{donor_id}")
def delete_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    db.delete(donor)
    db.commit()
    return {"message": "Donor deleted"}
