from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import BloodRequest
from app.models.user import User


router = APIRouter()


# Get dashboard stats
@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_donors = db.query(User).filter(User.role == "donor").count()
    total_requests = db.query(BloodRequest).count()
    pending_requests = db.query(BloodRequest).filter(BloodRequest.status == "pending").count()
    approved_requests = db.query(BloodRequest).filter(BloodRequest.status == "approved").count()
    
    return {
        "totalDonors": total_donors,
        "totalRequests": total_requests,
        "pendingRequests": pending_requests,
        "approvedRequests": approved_requests
    }


# Get all donors - FIXED: Query User table with role="donor"
@router.get("/donors")
def get_all_donors(db: Session = Depends(get_db)):
    donors = db.query(User).filter(User.role == "donor").all()
    return donors


# Delete a donor - FIXED: Delete from User table
@router.delete("/donors/{donor_id}")
def delete_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(User).filter(User.id == donor_id, User.role == "donor").first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    db.delete(donor)
    db.commit()
    return {"message": "Donor deleted successfully"}


# Get all blood requests
@router.get("/requests")
def get_all_requests(db: Session = Depends(get_db)):
    requests = db.query(BloodRequest).all()
    return requests


# Approve or reject a request
@router.put("/requests/{request_id}")
def update_request_status(request_id: int, status: str, db: Session = Depends(get_db)):
    request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request.status = status
    db.commit()
    return {"message": f"Request {status} successfully"}