from pydantic import BaseModel

class GuideRequest(BaseModel):
    question: str