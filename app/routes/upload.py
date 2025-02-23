from fastapi import APIRouter, File, UploadFile, HTTPException
from app.database import requests_collection
from app.worker import task_queue, process_request_in_background
from app.models import StatusResponse
import uuid
import csv
from io import StringIO

router = APIRouter()

@router.post("/upload", response_model=StatusResponse)
async def upload_csv(file: UploadFile = File(...), webhook_url: str = None):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="CSV file is empty.")

    text_stream = StringIO(content.decode("utf-8"))
    reader = csv.reader(text_stream, skipinitialspace=True)
    all_rows = list(reader)

    if len(all_rows) < 2:
        raise HTTPException(status_code=400, detail="CSV must have at least one data row.")

    product_entries = []
    for row in all_rows[1:]:
        if len(row) < 3:
            continue
        product_entries.append({
            "serial_number": int(row[0].strip()),
            "product_name": row[1].strip(),
            "input_image_urls": [u.strip() for u in row[2].split(",") if u.strip()],
            "output_image_urls": []
        })

    request_id = str(uuid.uuid4())
    await requests_collection.insert_one({"request_id": request_id, "status": "pending", "product_entries": product_entries})

    task_queue.put((process_request_in_background, (request_id, webhook_url)))

    return StatusResponse(request_id=request_id, status="pending")
