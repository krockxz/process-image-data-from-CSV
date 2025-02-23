```md
# FastAPI Image Processing System

## Overview
This project is a FastAPI-based image processing system that:
- Uploads a CSV file containing product details and image URLs.
- Asynchronously downloads and compresses images to 50% quality.
- Stores processed image data in MongoDB Atlas.
- Provides an API to check the status of processing.
- Triggers a webhook once image processing is completed.

---

## Features
- Asynchronous background processing using worker threads.
- Image compression reduces file size by 50%.
- MongoDB Atlas integration to store processing status.
- Webhook support to notify clients when processing is complete.
- FastAPI-based REST APIs.

---

## Installation and Setup

### Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/fastapi-image-processing.git
cd fastapi-image-processing
```

### Create a Virtual Environment
```bash
python -m venv venv
```

### Activate the Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file in the project root and add:
```
MONGO_CONNECTION_STRING=mongodb+srv://kunal:kunal1234@menudb.oljtc.mongodb.net/?retryWrites=true&w=majority&appName=menuDB
DATABASE_NAME=image_processing_db
COLLECTION_NAME=requests
```

### Start the FastAPI Server
```bash
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc API Docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Documentation

### Upload CSV API
#### Endpoint
```http
POST /api/upload
```
#### Request Format (Multipart/Form-Data)
| Field        | Type       | Required | Description |
|-------------|-----------|----------|-------------|
| `file`      | File (CSV) | Yes      | The CSV file containing product details. |
| `webhook_url` | String (URL) | No  | Webhook URL to notify when processing is completed. |

#### Example CSV File (`test.csv`)
```csv
S. No.,Product Name,Input Image Urls
1,SKU1,https://picsum.photos/200/300, https://picsum.photos/200/301
2,SKU2,https://picsum.photos/200/302
```

#### Example Request
```bash
curl -X POST "http://localhost:8000/api/upload" -F "file=@test.csv"
```

#### Success Response (`200 OK`)
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending"
}
```

---

### Status Check API
#### Endpoint
```http
GET /api/status?request_id=<request_id>
```

#### Example Request
```http
GET http://localhost:8000/api/status?request_id=123e4567-e89b-12d3-a456-426614174000
```

#### Response (Processing Completed - `200 OK`)
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "details": [
    {
      "serial_number": 1,
      "product_name": "SKU1",
      "input_image_urls": [
        "https://picsum.photos/200/300",
        "https://picsum.photos/200/301"
      ],
      "output_image_urls": [
        "http://localhost:8000/compressed_images/output1.jpg",
        "http://localhost:8000/compressed_images/output2.jpg"
      ]
    }
  ]
}
```

---

### Webhook API
#### Endpoint
```http
POST /api/webhook-test
```
#### Request Format (JSON Body)
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed"
}
```
#### Success Response (`200 OK`)
```json
{
  "message": "Webhook received",
  "receivedPayload": {
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "completed"
  }
}
```

---

## Asynchronous Worker Documentation
This system processes images asynchronously using background worker threads.

### Worker Architecture
```mermaid
graph TD;
    MongoDB[(MongoDB Atlas)] -->|Triggers Worker| Worker[Background Worker]
    Worker -->|Fetches Images| Downloader[Image Downloader]
    Downloader -->|Compresses Images| ImageProcessor[Image Compression]
    ImageProcessor -->|Stores Compressed Images| Storage[(Compressed Image Folder)]
    Worker -->|Updates MongoDB| MongoDB
    Worker -->|Triggers Webhook| Webhook[ Client Webhook]
```

### How the Worker Works
1. Listens for new processing requests in MongoDB.
2. Downloads images from provided URLs.
3. Compresses images using PIL (50% quality reduction).
4. Stores compressed images locally.
5. Updates MongoDB with processed data.
6. Triggers a webhook if provided.

---

## Environment Configuration
The application requires MongoDB Atlas connection. The following credentials should be added to a `.env` file:

```
MONGO_CONNECTION_STRING=mongodb+srv://kunal:kunal1234@menudb.oljtc.mongodb.net/?retryWrites=true&w=majority&appName=menuDB
DATABASE_NAME=image_processing_db
COLLECTION_NAME=requests
```

---
