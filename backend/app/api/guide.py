from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.schemas.request import GuideRequest
from app.services.guide_service import GuideService

router = APIRouter(
    prefix="/guide",
    tags=["Career Guide"]
)


# Generate Guide
@router.post("/generate")
def generate_guide(request: GuideRequest):
    return GuideService.generate(request.question)


# Download PDF
@router.get("/download/{filename}")
def download_pdf(filename: str):
    return FileResponse(
        path=f"generated_guides/{filename}",
        media_type="application/pdf",
        filename=filename,
    )