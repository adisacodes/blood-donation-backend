from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import BloodRequest
from app.schemas import (
    BloodRequestCreate,
    BloodRequestUpdate,
    BloodRequestResponse
)

router = APIRouter()



@router.post("/", response_model=BloodRequestResponse, status_code=status.HTTP_201_CREATED)
def create_blood_request(
    request: BloodRequestCreate,
    db: Session = Depends(get_db)
):
    db_request = BloodRequest(
        requested_by=request.requested_by,
        blood_type=request.blood_type,
        units=request.units,
        date=request.date,
        status="pending"
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request



@router.get("/", response_model=List[BloodRequestResponse])
def get_all_blood_requests(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(BloodRequest)
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.get("/{request_id}", response_model=BloodRequestResponse)
def get_blood_request_by_id(
    request_id: int,
    db: Session = Depends(get_db)
):
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )

    return blood_request



@router.put("/{request_id}", response_model=BloodRequestResponse)
def update_blood_request(
    request_id: int,
    request_update: BloodRequestUpdate,
    db: Session = Depends(get_db)
):
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )

    update_data = request_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(blood_request, key, value)

    db.commit()
    db.refresh(blood_request)
    return blood_request



@router.post("/{request_id}/approve", response_model=BloodRequestResponse)
def approve_blood_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )
    
    if blood_request.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve a request that is already '{blood_request.status}'"
        )

    blood_request.status = "approved"
    db.commit()
    db.refresh(blood_request)
    return blood_request




@router.post("/{request_id}/reject", response_model=BloodRequestResponse)
def reject_blood_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )
        
    if blood_request.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reject a request that is already '{blood_request.status}'"
        )

    blood_request.status = "rejected"
    db.commit()
    db.refresh(blood_request)
    return blood_request



@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blood_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not blood_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood request not found"
        )

    db.delete(blood_request)
    db.commit()

