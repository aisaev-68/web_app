from fastapi import APIRouter

from app.api.api_v1.endpoints import form

api_router = APIRouter()

api_router.include_router(form.router, prefix="", tags=["forms"])

