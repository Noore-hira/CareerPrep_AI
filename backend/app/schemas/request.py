from pydantic import BaseModel

class GuideRequest(BaseModel):
    question: str
    model: str
    api_key: str