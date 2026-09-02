import pytest
from app.database.database import init_db, upsert_user, save_review, get_reviews, get_review


def test_init_db_and_user_upsert():
    init_db()
    user_id = upsert_user("123456", "testuser", "ghp_fake_token")
    assert isinstance(user_id, int)
    assert user_id > 0

    # Second upsert should update existing user and return same ID
    user_id_2 = upsert_user("123456", "testuser_updated", "ghp_new_token")
    assert user_id == user_id_2


def test_save_and_get_reviews():
    init_db()
    user_id = upsert_user("789012", "reviewer", "ghp_reviewer_token")

    summary = {
        "overall_score": "9.0/10",
        "recommendation": "Approve",
        "critical": 0,
        "high": 0,
        "medium": 1,
        "low": 2,
        "agents_reviewed": 6
    }
    results = [{"agent": "SecurityAgent", "analysis": "No critical vulnerabilities found."}]

    review_id = save_review(
        owner="octocat",
        repo="hello-world",
        pull_request=42,
        summary=summary,
        results=results,
        report_path="reports/hello-world_PR_42_Report.md",
        user_id=user_id
    )

    assert review_id > 0

    # Test user-scoped get_reviews
    user_reviews = get_reviews(user_id=user_id)
    assert len(user_reviews) > 0
    assert user_reviews[0]["repo"] == "hello-world"

    # Test single review fetch
    review_detail = get_review(review_id)
    assert review_detail is not None
    assert review_detail["overall_score"] == "9.0/10"
