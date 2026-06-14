from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Donor


from app.schemas.schemas import DonorCreate, DonorUpdate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_donor(donor_data: DonorCreate, db: Session = Depends(get_db)):
    donor = Donor(
        blood_type=donor_data.blood_type,
        location=donor_data.location,
        user_id=donor_data.user_id
    )
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
def update_donor(donor_id: int, donor_data: DonorUpdate, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")

    donor.blood_type = donor_data.blood_type
    donor.location = donor_data.location

    db.commit()
    db.refresh(donor)
    return donor


@router.delete("/{donor_id}")
def delete_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    db.delete(donor)
    db.commit()
    return {"message": "Donor deleted"}
