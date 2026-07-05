from fastapi import FastAPI
from app.api.guide import router as guide_router
from app.api.health import router as health_router

app = FastAPI(
    title="CareerPrep AI",
    description="AI Powered Career Guide Generator",
    version="2.0.0",
)

app.include_router(guide_router)
app.include_router(health_router)


@app.get("/")
def root():

    return {
        "message": "CareerPrep AI Backend Running"
    }
