from app.github.client import get_github_client


def get_pull_requests(owner: str, repo_name: str, token: str | None = None):
    """
    Fetch all open pull requests of a repository.
    """
    client = get_github_client(token)
    repo = client.get_repo(f"{owner}/{repo_name}")

    pull_requests = []

    for pr in repo.get_pulls(state="all"):
        pull_requests.append(
            {
                "number": pr.number,
                "title": pr.title,
                "author": pr.user.login,
                "created_at": pr.created_at,
            }
        )

    return pull_requests