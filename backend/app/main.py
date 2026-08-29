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
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise the database (creates tables on first run)
init_db()

# Mount all API routes
app.include_router(router)
