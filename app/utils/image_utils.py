import requests
import os
import uuid
import shutil
from PIL import Image
from app.config import OUTPUT_FOLDER

def compress_and_save_image(image_url: str, quality: int = 50) -> str:
 
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()  # ✅ Check for HTTP errors

    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to download {image_url}: {e}")
        return "" 

    temp_filename = f"temp_{uuid.uuid4()}.jpg"
    with open(temp_filename, "wb") as temp_file:
        shutil.copyfileobj(response.raw, temp_file)

    compressed_filename = f"{uuid.uuid4()}.jpg"
    compressed_filepath = os.path.join(OUTPUT_FOLDER, compressed_filename)

    try:
        with Image.open(temp_filename) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")

            img.save(compressed_filepath, format="JPEG", optimize=True, quality=quality)

    except Exception as e:
        print(f"[Error] Could not compress image {image_url}: {e}")
        return ""

    os.remove(temp_filename)

    return f"http://localhost:8000/compressed_images/{compressed_filename}"
