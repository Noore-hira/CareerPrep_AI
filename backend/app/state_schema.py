from pydantic import BaseModel
from typing import Optional


class GuideState(BaseModel):
    question: str

    # User-selected Groq settings
    model: str
    api_key: str

    role: Optional[str] = None
    continue_pipeline: Optional[bool] = None
    response: Optional[str] = None

    intro_response: Optional[str] = None
    rcs_response: Optional[str] = None
    rm_response: Optional[str] = None
    iv_response: Optional[str] = None
    pj_response: Optional[str] = None

    merge_response: Optional[str] = None
    pdf_path: Optional[str] = None