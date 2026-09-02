from app.github.client import get_github_client


def get_repositories(token: str | None = None):
    """
    Fetch all repositories for the authenticated user (or fallback client).
    """
    client = get_github_client(token)
    user = client.get_user()

    repositories = []

    for repo in user.get_repos():
        repositories.append(
            {
                "name": repo.name,
                "owner": repo.owner.login,
                "private": repo.private,
                "default_branch": repo.default_branch,
            }
        )

    return repositories