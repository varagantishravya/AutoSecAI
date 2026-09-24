from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.database.database import init_db

app = FastAPI(
    title="AutoSecAI",
    description="A Multi-Agent LLM Framework for Intelligent Pull Request Review",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise the database (creates tables on first run)
init_db()

# Mount all API routes
from app.api.auth import router as auth_router
app.include_router(auth_router, prefix="/auth")
app.include_router(router)
