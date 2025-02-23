from fastapi import APIRouter, Request
from app.database import requests_collection

router = APIRouter()

@router.post("/webhook")
async def webhook_receiver(request: Request):

    try:
        payload = await request.json()
        print("[Webhook] Received:", payload)

        webhook_event = {
            "request_id": payload.get("request_id"),
            "status": payload.get("status"),
            "event_data": payload  
        }
        await requests_collection.update_one(
            {"request_id": payload.get("request_id")},
            {"$set": {"webhook_event": webhook_event}}
        )

        return {"message": "Webhook received", "status": "success"}
    except Exception as e:
        print("[Webhook Error]", e)
        return {"message": "Webhook processing failed", "error": str(e)}
