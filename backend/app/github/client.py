import os
from dotenv import load_dotenv
from github import Github, GithubException

load_dotenv()

# Server default token (fallback for local dev if user token not provided)
DEFAULT_GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_client(token: str | None = None) -> Github:
    """
    Returns a PyGithub Github client.
    Prefers the user-provided access token; falls back to DEFAULT_GITHUB_TOKEN.
    """
    effective_token = token or DEFAULT_GITHUB_TOKEN
    if not effective_token:
        raise ValueError("No GitHub token provided and GITHUB_TOKEN not set in environment.")
    return Github(effective_token)

# Backward-compatibility alias
github_client = get_github_client(DEFAULT_GITHUB_TOKEN) if DEFAULT_GITHUB_TOKEN else None

def get_authenticated_user_info(token: str) -> dict:
    """
    Fetch GitHub user details for a given access token.
    """
    client = get_github_client(token)
    user = client.get_user()
    return {
        "github_id": str(user.id),
        "username": user.login,
        "name": user.name or user.login,
        "avatar_url": user.avatar_url,
    }