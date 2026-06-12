from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_requests():
    return {"message": "Requests router working!"}