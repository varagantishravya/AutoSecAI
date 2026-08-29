import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_pull_request_files(owner, repo, pr_number):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()