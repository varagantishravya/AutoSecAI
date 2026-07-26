from fastapi.responses import FileResponse
import os
from fastapi import FastAPI
from app.models.review import ReviewRequest
from app.coordinator.coordinator import CoordinatorAgent
from app.github.repositories import get_repositories
from app.github.pull_requests import get_pull_requests
from app.github.changed_files import get_changed_files
app = FastAPI(
    title="AutoSecAI",
    description="A Multi-Agent LLM Framework for Intelligent Pull Request Review",
    version="1.0.0"
)

coordinator = CoordinatorAgent()


@app.get("/")
def home():
    return {"message": "Welcome to AutoSecAI Version 1 🚀"}


@app.get("/health")
def health():
    return {"status": "Running Successfully"}


@app.get("/repositories")
def repositories():
    return get_repositories()


@app.get("/pull-requests")
def pull_requests(owner: str, repo: str):
    return get_pull_requests(owner, repo)

@app.get("/changed-files")
def changed_files(owner: str, repo: str, pull_request: int):
    return get_changed_files(owner, repo, pull_request)

@app.post("/review")
def review_pull_request(request: ReviewRequest):
    print("========== REVIEW REQUEST RECEIVED ==========")

    return coordinator.review_pull_request(
        request.owner,
        request.repository,
        request.pull_request
    )

@app.get("/download-report")
def download_report():

    file_path = "reports/AutoSecAI_PR_1_Report.md"

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="AutoSecAI_PR_1_Report.md",
            media_type="text/markdown"
        )

    return {"error": "Report not found"}

