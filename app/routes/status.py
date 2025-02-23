from fastapi import APIRouter, HTTPException
from app.database import requests_collection
from app.models import StatusResponse

router = APIRouter()

@router.get("/status", response_model=StatusResponse)
async def get_status(request_id: str):

    doc = await requests_collection.find_one({"request_id": request_id})
    
    if not doc:
        raise HTTPException(status_code=404, detail="Request not found")

    return StatusResponse(
        request_id=request_id,
        status=doc["status"],
        details=doc.get("product_entries", [])
    )
