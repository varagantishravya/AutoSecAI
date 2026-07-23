from app.github.client import github_client


def get_repositories():
    """
    Fetch all repositories for the authenticated user.
    """
    user = github_client.get_user()

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