import asyncio
import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import chatroom, users

load_dotenv()

MODE = os.getenv("MODE", "dev")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "4000"))
SERVER_WORKERS = int(os.getenv("SERVER_WORKERS", "1"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI(
    title="API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

logger.info("Add middleware")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Include routers")
app.include_router(users.router)
app.include_router(chatroom.router)


def run_backend():
    uvicorn.run(
        app="backend.main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        proxy_headers=True,
        workers=SERVER_WORKERS,
        log_level="info",
        reload=True if MODE == "dev" else False,
    )
    print("backend is up")


if __name__ == "__main__":
    run_backend()
