from pydantic import BaseModel
from typing import Optional

class GuideResponse(BaseModel):
    status: str
    role: Optional[str] = None
    response: Optional[str] = None
    pdf_path: Optional[str] = None