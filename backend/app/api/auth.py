import os
import requests
from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.github.client import get_authenticated_user_info
from app.database.database import upsert_user

router = APIRouter()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


class PATRequest(BaseModel):
    token: str


def get_token_from_header(authorization: str = Header(None)) -> str | None:
    if not authorization:
        return None
    if authorization.startswith("Bearer "):
        return authorization.split("Bearer ")[1].strip()
    return authorization.strip()


@router.get("/login/github")
def github_login():
    if not GITHUB_CLIENT_ID:
        raise HTTPException(
            status_code=400,
            detail="GitHub Client ID is not configured in backend/.env. Please use Personal Access Token login instead."
        )
    
    redirect_uri = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=repo,user"
    return RedirectResponse(redirect_uri)


@router.get("/callback/github")
def github_callback(code: str):
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        raise HTTPException(status_code=400, detail="GitHub credentials not configured")
        
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get access token from GitHub")
        
    access_token = response.json().get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="No access token in response")
        
    # Fetch user info and upsert into database
    try:
        user_info = get_authenticated_user_info(access_token)
        upsert_user(user_info["github_id"], user_info["username"], access_token)
    except Exception as e:
        print(f"Warning: Failed to upsert user on OAuth callback: {e}")
    
    return RedirectResponse(f"{FRONTEND_URL}?token={access_token}")


@router.get("/me")
def get_current_user(token: str | None = Depends(get_token_from_header)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization token")
    
    try:
        user_info = get_authenticated_user_info(token)
        user_id = upsert_user(user_info["github_id"], user_info["username"], token)
        return {
            "id": user_id,
            "github_id": user_info["github_id"],
            "username": user_info["username"],
            "name": user_info["name"],
            "avatar_url": user_info["avatar_url"],
            "token": token
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid GitHub Token: {str(e)}")


@router.post("/pat")
def login_with_pat(request: PATRequest):
    token = request.token.strip()
    if not token:
        raise HTTPException(status_code=400, detail="Token cannot be empty")
    
    try:
        user_info = get_authenticated_user_info(token)
        user_id = upsert_user(user_info["github_id"], user_info["username"], token)
        return {
            "id": user_id,
            "github_id": user_info["github_id"],
            "username": user_info["username"],
            "name": user_info["name"],
            "avatar_url": user_info["avatar_url"],
            "token": token
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to authenticate with token: {str(e)}")

