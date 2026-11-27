from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, customers, invoices


api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(customers.router)
api_router.include_router(invoices.router)