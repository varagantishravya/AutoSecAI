from app.github.client import get_github_client


def post_pr_comment(owner: str, repo_name: str, pr_number: int, comment_body: str, token: str | None = None) -> dict:
    """
    Post a comment on a GitHub Pull Request.
    """
    client = get_github_client(token)
    repo = client.get_repo(f"{owner}/{repo_name}")
    pull_request = repo.get_pull(pr_number)
    
    comment = pull_request.create_issue_comment(comment_body)
    return {
        "status": "success",
        "comment_id": comment.id,
        "comment_url": comment.html_url,
    }
