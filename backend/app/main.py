from fastapi import FastAPI
from app.config import settings
from app.api.router import api_router
from app.utils.exception_handler import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-agent AI system for billing investigation and dispute resolution.",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "AI Billing & Dispute Resolution System is running",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
    }
