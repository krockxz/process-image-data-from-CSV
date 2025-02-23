from pydantic import BaseModel, Field
from typing import Optional, List

class ProductEntry(BaseModel):
    serial_number: int = Field(..., alias="S. No.")
    product_name: str = Field(..., alias="Product Name")
    input_image_urls: str = Field(..., alias="Input Image Urls")

class StatusResponse(BaseModel):
    request_id: str
    status: str
    details: Optional[List[dict]] = None
