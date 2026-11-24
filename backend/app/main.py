from fastapi import FastAPI
from app.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-agent AI system for billing investigation and dispute resolution.",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


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
