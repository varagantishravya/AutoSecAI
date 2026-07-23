from app.github.client import github_client


def get_changed_files(owner: str, repo_name: str, pr_number: int):
    """
    Fetch all changed files from a pull request.
    """

    repo = github_client.get_repo(f"{owner}/{repo_name}")

    pull_request = repo.get_pull(pr_number)

    changed_files = []

    for file in pull_request.get_files():

        changed_files.append(
            {
                "filename": file.filename,
                "status": file.status,
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes,
                "patch": file.patch,
            }
        )

    return changed_files