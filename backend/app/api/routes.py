"""
AutoSecAI — API Routes
=======================
Modular FastAPI router containing all application endpoints.

Endpoints:
    GET  /                  — Welcome message
    GET  /health            — Health-check
    GET  /repositories      — List GitHub repositories
    GET  /pull-requests     — List open PRs for a repository
    GET  /changed-files     — List files changed in a PR
    POST /review            — Run a multi-agent PR review
    GET  /download-report   — Download the Markdown report
    GET  /review-history    — List past reviews (from database)
    GET  /review-history/{id} — Get a single review by ID
"""

import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.coordinator.coordinator import CoordinatorAgent
from app.database.database import get_review, get_reviews
from app.github.changed_files import get_changed_files
from app.github.pull_requests import get_pull_requests
from app.github.repositories import get_repositories
from app.models.review import ReviewRequest

# Resolve the project root (backend/) regardless of where uvicorn is launched from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

router = APIRouter()
coordinator = CoordinatorAgent()


# ── General ────────────────────────────────────────────────────────────


@router.get("/")
def home():
    return {"message": "Welcome to AutoSecAI Version 1 🚀"}


@router.get("/health")
def health():
    return {"status": "Running Successfully"}


# ── GitHub ─────────────────────────────────────────────────────────────


@router.get("/repositories")
def list_repositories():
    return get_repositories()


@router.get("/pull-requests")
def list_pull_requests(owner: str, repo: str):
    return get_pull_requests(owner, repo)


@router.get("/changed-files")
def list_changed_files(owner: str, repo: str, pull_request: int):
    return get_changed_files(owner, repo, pull_request)


# ── Review ─────────────────────────────────────────────────────────────


@router.post("/review")
def review_pull_request(request: ReviewRequest):
    print("========== REVIEW REQUEST RECEIVED ==========")
    return coordinator.review_pull_request(
        request.owner,
        request.repository,
        request.pull_request,
    )


@router.get("/download-report")
def download_report(repo: str, pull_request: int):
    """
    Download the generated Markdown report for a specific repository and PR.

    Query params:
        repo          - repository name (e.g. AutoSecAI)
        pull_request  - pull request number (e.g. 5)
    """
    filename = f"{repo}_PR_{pull_request}_Report.md"
    file_path = os.path.join(REPORTS_DIR, filename)

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="text/markdown",
        )

    raise HTTPException(
        status_code=404,
        detail=f"Report not found: {filename}. Run a review first.",
    )


# ── Review History ─────────────────────────────────────────────────────


@router.get("/review-history")
def review_history(limit: int = 50):
    """Return the most recent reviews from the database."""
    return get_reviews(limit=limit)


@router.get("/review-history/{review_id}")
def review_detail(review_id: int):
    """Return full details for a single review."""
    review = get_review(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found.")
    return review
