import os

from dotenv import load_dotenv
from github import Github

# Load variables from .env
load_dotenv()

# Read GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in .env file")

# Create GitHub client
github_client = Github(GITHUB_TOKEN)