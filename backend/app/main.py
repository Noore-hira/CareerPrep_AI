import config_cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.guide import router as guide_router
from app.api.health import router as health_router


app = FastAPI(
    title="CareerPrep AI",
    description="AI Powered Career Guide Generator",
    version="2.0.0",
)


# Frontend URLs allowed to access backend
ALLOWED_ORIGINS = [
    "https://career-prep-ai-6ylv-career-prep-ai.vercel.app",
    "https://career-prep-ai-6ylv-git-main-career-prep-ai.vercel.app",
    "https://career-prep-ai-6ylv-n5xsniucp-career-prep-ai.vercel.app",

    # Local development
    "http://localhost:5173",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(guide_router)
app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "CareerPrep AI Backend Running"
    }