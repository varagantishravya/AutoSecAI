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
from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.responses import FileResponse

from app.coordinator.coordinator import CoordinatorAgent
from app.database.database import get_review, get_reviews, upsert_user
from app.github.changed_files import get_changed_files
from app.github.pull_requests import get_pull_requests
from app.github.repositories import get_repositories
from app.github.client import get_authenticated_user_info
from app.github.comments import post_pr_comment
from app.models.review import ReviewRequest, CommentRequest


# Resolve the project root (backend/) regardless of where uvicorn is launched from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

router = APIRouter()
coordinator = CoordinatorAgent()


def get_token(authorization: str = Header(None)) -> str | None:
    if not authorization:
        return None
    if authorization.startswith("Bearer "):
        return authorization.split("Bearer ")[1].strip()
    return authorization.strip()


def get_user_context(token: str | None = Depends(get_token)):
    user_id = None
    if token:
        try:
            user_info = get_authenticated_user_info(token)
            user_id = upsert_user(user_info["github_id"], user_info["username"], token)
        except Exception as e:
            print(f"Token user resolution notice: {e}")
    return {"token": token, "user_id": user_id}


# ── General ────────────────────────────────────────────────────────────


@router.get("/")
def home():
    return {"message": "Welcome to AutoSecAI Version 1 🚀"}


@router.get("/health")
def health():
    return {"status": "Running Successfully"}


# ── GitHub ─────────────────────────────────────────────────────────────


@router.get("/repositories")
def list_repositories(ctx: dict = Depends(get_user_context)):
    return get_repositories(token=ctx["token"])


@router.get("/pull-requests")
def list_pull_requests(owner: str, repo: str, ctx: dict = Depends(get_user_context)):
    return get_pull_requests(owner, repo, token=ctx["token"])


@router.get("/changed-files")
def list_changed_files(owner: str, repo: str, pull_request: int, ctx: dict = Depends(get_user_context)):
    return get_changed_files(owner, repo, pull_request, token=ctx["token"])


# ── Review ─────────────────────────────────────────────────────────────


@router.post("/review")
def review_pull_request(request: ReviewRequest, ctx: dict = Depends(get_user_context)):
    print("========== REVIEW REQUEST RECEIVED ==========")
    return coordinator.review_pull_request(
        request.owner,
        request.repository,
        request.pull_request,
        token=ctx["token"],
        user_id=ctx["user_id"],
    )


@router.post("/post-comment")
def post_review_comment(request: CommentRequest, ctx: dict = Depends(get_user_context)):
    print("========== POST PR COMMENT REQUEST ==========")
    try:
        return post_pr_comment(
            owner=request.owner,
            repo_name=request.repository,
            pr_number=request.pull_request,
            comment_body=request.comment,
            token=ctx["token"],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to post comment to GitHub: {str(e)}")



@router.get("/download-report")
def download_report(repo: str, pull_request: int):
    """
    Download the generated Markdown report for a specific repository and PR.
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
def review_history(limit: int = 50, ctx: dict = Depends(get_user_context)):
    """Return the most recent reviews from the database for the current user."""
    return get_reviews(user_id=ctx["user_id"], limit=limit)


@router.get("/review-history/{review_id}")
def review_detail(review_id: int):
    """Return full details for a single review."""
    review = get_review(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found.")
    return review

