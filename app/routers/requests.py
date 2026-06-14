from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import BloodRequest, Donor
from app.schemas import (
    BloodRequestCreate, 
    BloodRequestUpdate, 
    BloodRequestResponse, 
    BloodRequestListResponse,
    DonorMatchResponse
)

router = APIRouter()


#  CREATE OPERATIONS 

@router.post("/", response_model=BloodRequestResponse, status_code=status.HTTP_201_CREATED)
def create_blood_request(
    request: BloodRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new blood request.
    
    - **patient_name**: Patient's full name
    - **blood_group**: Required blood type (A+, A-, B+, B-, AB+, AB-, O+, O-)
    - **units_needed**: Number of units (1-100)
    - **hospital**: Hospital name
    - **location**: City/District
    - **contact_number**: Contact phone number
    - **urgency**: Urgency level (Low, Medium, High, Critical)
    - **medical_condition**: Medical condition details
    - **notes**: Additional notes
    """
    db_request = BloodRequest(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


#  READ OPERATIONS 

@router.get("/", response_model=List[BloodRequestListResponse])
def get_all_blood_requests(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    blood_group: Optional[str] = Query(None),
    urgency: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(True),
):
    """
    Get all blood requests with optional filtering and pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 10, max: 100)
    - **blood_group**: Filter by blood group
    - **urgency**: Filter by urgency level
    - **status**: Filter by status (Pending, Fulfilled, Cancelled, Expired)
    - **is_active**: Filter by active status (default: True)
    """
    query = db.query(BloodRequest)

    if is_active is not None:
        query = query.filter(BloodRequest.is_active == is_active)
    
    if blood_group:
        query = query.filter(BloodRequest.blood_group == blood_group)
    
    if urgency:
        query = query.filter(BloodRequest.urgency == urgency)
    
    if status:
        query = query.filter(BloodRequest.status == status)

    requests = query.order_by(desc(BloodRequest.created_at)).offset(skip).limit(limit).all()
    return requests


@router.get("/search/", response_model=List[BloodRequestListResponse])
def search_blood_requests(
    db: Session = Depends(get_db),
    query_text: str = Query(..., min_length=1),
    blood_group: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
):
    """
    Search blood requests by patient name, hospital, or contact.
    
    - **query_text**: Search term
    - **blood_group**: Optional blood group filter
    - **limit**: Maximum results
    """
    search_pattern = f"%{query_text}%"
    
    query_obj = db.query(BloodRequest).filter(
        or_(
            BloodRequest.patient_name.ilike(search_pattern),
            BloodRequest.hospital.ilike(search_pattern),
            BloodRequest.contact_number.ilike(search_pattern)
        )
    )

    if blood_group:
        query_obj = query_obj.filter(BloodRequest.blood_group == blood_group)

    requests = query_obj.limit(limit).all()
    return requests


@router.get("/blood-group/{blood_group}", response_model=List[BloodRequestListResponse])
def get_requests_by_blood_group(
    blood_group: str,
    db: Session = Depends(get_db),
    urgency: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Get all pending blood requests for a specific blood group.
    
    - **blood_group**: Blood type
    - **urgency**: Optional urgency filter
    - **limit**: Maximum records
    """
    valid_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if blood_group not in valid_groups:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid blood group. Must be one of: {', '.join(valid_groups)}"
        )

    query_obj = db.query(BloodRequest).filter(
        BloodRequest.blood_group == blood_group,
        BloodRequest.status == "Pending",
        BloodRequest.is_active == True
    )

    if urgency:
        query_obj = query_obj.filter(BloodRequest.urgency == urgency)

    requests = query_obj.order_by(desc(BloodRequest.urgency)).limit(limit).all()
    return requests


@router.get("/location/{location}", response_model=List[BloodRequestListResponse])
def get_requests_by_location(
    location: str,
    db: Session = Depends(get_db),
    status_filter: Optional[str] = Query(None),
):
    """
    Get blood requests by location.
    
    - **location**: City/District name
    - **status_filter**: Optional status filter
    """
    query_obj = db.query(BloodRequest).filter(
        BloodRequest.location.ilike(f"%{location}%"),
        BloodRequest.is_active == True
    )

    if status_filter:
        query_obj = query_obj.filter(BloodRequest.status == status_filter)

    requests = query_obj.order_by(desc(BloodRequest.urgency)).all()
    return requests


@router.get("/urgent/", response_model=List[BloodRequestListResponse])
def get_urgent_requests(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Get all critical and high urgency pending requests.
    """
    requests = db.query(BloodRequest).filter(
        BloodRequest.status == "Pending",
        BloodRequest.is_active == True,
        BloodRequest.urgency.in_(["Critical", "High"])
    ).order_by(desc(BloodRequest.urgency)).limit(limit).all()
    
    return requests


@router.get("/{request_id}", response_model=BloodRequestResponse)
def get_blood_request_by_id(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific blood request by ID.
    """
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    
    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )
    
    return blood_request


# ==================== UPDATE OPERATIONS ====================

@router.put("/{request_id}", response_model=BloodRequestResponse)
def update_blood_request(
    request_id: int,
    request_update: BloodRequestUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a blood request.
    """
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    
    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )

    update_data = request_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(blood_request, field, value)

    db.add(blood_request)
    db.commit()
    db.refresh(blood_request)
    return blood_request


@router.patch("/{request_id}/status", response_model=BloodRequestResponse)
def update_request_status(
    request_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):
    """
    Update blood request status.
    
    Valid statuses: Pending, Fulfilled, Cancelled, Expired
    """
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    
    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )

    valid_statuses = ["Pending", "Fulfilled", "Cancelled", "Expired"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    blood_request.status = new_status
    
    if new_status == "Fulfilled":
        blood_request.fulfilled_date = datetime.utcnow()
        blood_request.units_fulfilled = blood_request.units_needed

    db.add(blood_request)
    db.commit()
    db.refresh(blood_request)
    return blood_request


@router.patch("/{request_id}/fulfill", response_model=BloodRequestResponse)
def fulfill_blood_request(
    request_id: int,
    units: int = Query(..., ge=1),
    db: Session = Depends(get_db)
):
    """
    Update blood request fulfillment with units count.
    """
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    
    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )

    if units > blood_request.units_needed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Units cannot exceed required units ({blood_request.units_needed})"
        )

    blood_request.units_fulfilled = units
    
    if units >= blood_request.units_needed:
        blood_request.status = "Fulfilled"
        blood_request.fulfilled_date = datetime.utcnow()

    db.add(blood_request)
    db.commit()
    db.refresh(blood_request)
    return blood_request


#  DELETE OPERATIONS 

@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blood_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Soft delete a blood request (marks as inactive).
    """
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    
    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )

    blood_request.is_active = False
    db.add(blood_request)
    db.commit()


#  DONOR MATCHING 

@router.get("/{request_id}/matching-donors/", response_model=List[DonorMatchResponse])
def find_matching_donors(
    request_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Find donors matching the blood request criteria.
    
    Returns donors with:
    - Matching blood group
    - Available donation status
    - Same location (preferred)
    - Verified status (preferred)
    """
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    
    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )

    # Get donors with exact blood group match
    exact_match_donors = db.query(Donor).filter(
        Donor.blood_group == blood_request.blood_group,
        Donor.donation_status == "Available",
        Donor.is_active == True,
        Donor.age >= 18,
        Donor.age <= 65
    ).all()

    # Sort: Same location + Verified first
    donors = []
    for donor in exact_match_donors:
        distance_match = "Same Location" if donor.location.lower() == blood_request.location.lower() else "Different Location"
        donors.append({
            "id": donor.id,
            "name": donor.name,
            "blood_group": donor.blood_group,
            "phone": donor.phone,
            "location": donor.location,
            "age": donor.age,
            "donation_status": donor.donation_status,
            "distance_match": distance_match,
            "is_verified": donor.is_verified,
            "sort_priority": (distance_match == "Same Location", donor.is_verified)
        })

    # Sort by priority
    donors.sort(key=lambda x: x["sort_priority"], reverse=True)
    
    # Remove sort_priority before returning
    for donor in donors:
        del donor["sort_priority"]

    return donors[:limit]


@router.get("/stats/donor-availability-for-request/{blood_group}", response_model=dict)
def get_donor_availability_for_blood_group(
    blood_group: str,
    db: Session = Depends(get_db),
):
    """
    Get donor availability statistics for a blood group.
    """
    valid_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if blood_group not in valid_groups:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid blood group. Must be one of: {', '.join(valid_groups)}"
        )

    available_donors = db.query(func.count(Donor.id)).filter(
        Donor.blood_group == blood_group,
        Donor.donation_status == "Available",
        Donor.is_active == True
    ).scalar() or 0

    verified_donors = db.query(func.count(Donor.id)).filter(
        Donor.blood_group == blood_group,
        Donor.donation_status == "Available",
        Donor.is_verified == True,
        Donor.is_active == True
    ).scalar() or 0

    pending_requests = db.query(func.count(BloodRequest.id)).filter(
        BloodRequest.blood_group == blood_group,
        BloodRequest.status == "Pending",
        BloodRequest.is_active == True
    ).scalar() or 0

    return {
        "blood_group": blood_group,
        "available_donors": available_donors,
        "verified_donors": verified_donors,
        "pending_requests": pending_requests,
        "donor_to_request_ratio": available_donors / pending_requests if pending_requests > 0 else available_donors
    }


# ANALYTICS & STATISTICS 

@router.get("/stats/summary/", response_model=dict)
def get_request_statistics(db: Session = Depends(get_db)):
    """
    Get blood request statistics and analytics.
    """
    total_requests = db.query(func.count(BloodRequest.id)).filter(BloodRequest.is_active == True).scalar() or 0
    pending_requests = db.query(func.count(BloodRequest.id)).filter(BloodRequest.status == "Pending").scalar() or 0
    fulfilled_requests = db.query(func.count(BloodRequest.id)).filter(BloodRequest.status == "Fulfilled").scalar() or 0
    cancelled_requests = db.query(func.count(BloodRequest.id)).filter(BloodRequest.status == "Cancelled").scalar() or 0

    # Blood group distribution
    blood_groups = db.query(
        BloodRequest.blood_group,
        func.count(BloodRequest.id).label("count")
    ).filter(BloodRequest.status == "Pending").group_by(BloodRequest.blood_group).all()

    blood_group_stats = {bg: count for bg, count in blood_groups}

    # Urgency distribution
    urgencies = db.query(
        BloodRequest.urgency,
        func.count(BloodRequest.id).label("count")
    ).filter(BloodRequest.status == "Pending").group_by(BloodRequest.urgency).all()

    urgency_stats = {urgency: count for urgency, count in urgencies}

    return {
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "fulfilled_requests": fulfilled_requests,
        "cancelled_requests": cancelled_requests,
        "blood_group_distribution": blood_group_stats,
        "urgency_distribution": urgency_stats,
        "fulfillment_rate": round((fulfilled_requests / total_requests * 100) if total_requests > 0 else 0, 2)
    }


@router.get("/stats/critical-needs/", response_model=dict)
def get_critical_blood_needs(db: Session = Depends(get_db)):
    """
    Get current critical blood needs across all locations.
    """
    critical_requests = db.query(
        BloodRequest.blood_group,
        BloodRequest.location,
        func.sum(BloodRequest.units_needed).label("total_units"),
        func.count(BloodRequest.id).label("request_count")
    ).filter(
        BloodRequest.urgency == "Critical",
        BloodRequest.status == "Pending",
        BloodRequest.is_active == True
    ).group_by(BloodRequest.blood_group, BloodRequest.location).all()

    result = []
    for bg, location, units, count in critical_requests:
        result.append({
            "blood_group": bg,
            "location": location,
            "total_units_needed": units,
            "request_count": count
        })

    return {"critical_needs": result}