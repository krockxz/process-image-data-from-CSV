import asyncio
import threading
import queue
from app.database import requests_collection
from app.utils.image_utils import compress_and_save_image
import requests

# Create a task queue for image processing
task_queue = queue.Queue()

# Get the main event loop
loop = asyncio.get_event_loop()

def worker_thread():
    """Worker function to process image compression tasks asynchronously."""
    while True:
        task_func, task_args = task_queue.get()
        try:
            future = asyncio.run_coroutine_threadsafe(task_func(*task_args), loop)
            future.result()  # ✅ Wait for the coroutine to finish
        except Exception as e:
            print(f"❌ [Worker Error] {e}")
        finally:
            task_queue.task_done()

# Start the worker thread
threading.Thread(target=worker_thread, daemon=True).start()

async def process_request_in_background(request_id: str, webhook_url: str = None):
    """
    Processes image compression tasks in the background asynchronously.
    """
    print(f"🔄 [Worker] Processing request {request_id}")

    try:
        # ✅ Fetch request details properly
        doc = await requests_collection.find_one({"request_id": request_id})

        if not doc:
            print(f"❌ [Worker] Request ID {request_id} not found")
            return

        product_entries = doc.get("product_entries", [])
        updated_entries = []

        for entry in product_entries:
            input_urls = entry.get("input_image_urls", [])
            output_urls = []

            for url in input_urls:
                compressed_url = compress_and_save_image(url)  # ✅ This function is synchronous
                output_urls.append(compressed_url)

            entry["output_image_urls"] = output_urls
            updated_entries.append(entry)

        # ✅ Update MongoDB in an async way
        await requests_collection.update_one(
            {"request_id": request_id},
            {"$set": {"status": "completed", "product_entries": updated_entries}}
        )

        print(f"✅ [Worker] Finished processing {request_id}")

        # ✅ Send webhook notification if applicable
        if webhook_url:
            try:
                requests.post(webhook_url, json={"request_id": request_id, "status": "completed"})
            except Exception as e:
                print(f"❌ [Webhook Error] {e}")

    except Exception as e:
        print(f"❌ [Worker Error] Unexpected issue processing request {request_id}: {e}")

