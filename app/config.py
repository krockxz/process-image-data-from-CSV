import os
from dotenv import load_dotenv

load_dotenv()

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "image_processing_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "requests")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "compressed_images")
WEBHOOK_TIMEOUT = int(os.getenv("WEBHOOK_TIMEOUT", 5))

# Create the output directory if it does not exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
