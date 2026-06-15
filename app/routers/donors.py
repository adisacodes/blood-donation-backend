from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

router = APIRouter()


# CREATE / REGISTER DONOR PROFILE
@router.post("/")
def create_donor(blood_type: str, location: str, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert user into donor role + store donor info
    user.role = "donor"
    user.blood_group = blood_type
    user.location = location

    db.commit()
    db.refresh(user)

    return {
        "message": "Donor created successfully",
        "user": user
    }


# GET ALL DONORS
@router.get("/")
def get_donors(blood_type: str = None, db: Session = Depends(get_db)):
    query = db.query(User).filter(User.role == "donor")

    if blood_type:
        query = query.filter(User.blood_group == blood_type)

    return query.all()


# UPDATE DONOR
@router.put("/{user_id}")
def update_donor(user_id: int, blood_type: str, location: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.role == "donor").first()

    if not user:
        raise HTTPException(status_code=404, detail="Donor not found")

    user.blood_group = blood_type
    user.location = location

    db.commit()
    db.refresh(user)

    return user


# DELETE DONOR (remove donor role, don't delete user)
@router.delete("/{user_id}")
def delete_donor(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.role == "donor").first()

    if not user:
        raise HTTPException(status_code=404, detail="Donor not found")

    # Instead of deleting, demote user
    user.role = "user"
    user.blood_group = None
    user.location = None

    db.commit()

    return {"message": "Donor removed successfully"}