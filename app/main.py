from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router as api_router_v1
from app.db import get_db

app = FastAPI(
    title="Test task",
    description="Тестовое задание.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url='/api/redoc',
)

origins = [
    "http://localhost",
    "http://127.0.0.1/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", get_db)
# app.add_event_handler("shutdown", close_db_connect)

app.include_router(api_router_v1)
