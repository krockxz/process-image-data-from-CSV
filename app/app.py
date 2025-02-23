from fastapi import FastAPI
from app.routes import upload, status, webhook

app = FastAPI(title="Image Processing API", version="1.0")

app.include_router(upload.router, prefix="/api")
app.include_router(status.router, prefix="/api")
app.include_router(webhook.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
