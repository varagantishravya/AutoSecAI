"""
AutoSecAI — Database Module
============================
Provides SQLite-backed persistence for review history.

Tables:
    reviews  — stores every completed PR review with scores, results, and metadata.

Usage:
    from app.database.database import init_db, save_review, get_reviews, get_review

    init_db()                           # call once at startup
    review_id = save_review(...)        # after each review
    rows      = get_reviews(limit=50)   # for the dashboard
    row       = get_review(review_id)   # single lookup
"""

import json
import os
import sqlite3
from datetime import datetime, timezone

# Store the DB file inside  backend/data/
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DATA_DIR = os.path.join(_BASE_DIR, "data")
_DB_PATH = os.path.join(_DATA_DIR, "autosecai.db")


def _get_connection() -> sqlite3.Connection:
    """Return a new connection with row-factory enabled."""
    os.makedirs(_DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the reviews table if it does not already exist."""
    conn = _get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                owner           TEXT    NOT NULL,
                repo            TEXT    NOT NULL,
                pull_request    INTEGER NOT NULL,
                overall_score   TEXT,
                recommendation  TEXT,
                critical        INTEGER DEFAULT 0,
                high            INTEGER DEFAULT 0,
                medium          INTEGER DEFAULT 0,
                low             INTEGER DEFAULT 0,
                agents_reviewed INTEGER DEFAULT 0,
                results_json    TEXT,
                report_path     TEXT,
                created_at      TEXT    NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_review(
    owner: str,
    repo: str,
    pull_request: int,
    summary: dict,
    results: list,
    report_path: str,
) -> int:
    """
    Persist a completed review and return its auto-generated ID.

    Args:
        owner:        GitHub repository owner.
        repo:         Repository name.
        pull_request: PR number.
        summary:      The parsed summary dict from CoordinatorAgent.
        results:      The list of all agent result dicts.
        report_path:  Filesystem path to the generated Markdown report.

    Returns:
        The integer row ID of the newly inserted review.
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            """
            INSERT INTO reviews
                (owner, repo, pull_request, overall_score, recommendation,
                 critical, high, medium, low, agents_reviewed,
                 results_json, report_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                owner,
                repo,
                pull_request,
                summary.get("overall_score", "N/A"),
                summary.get("recommendation", "N/A"),
                summary.get("critical", 0),
                summary.get("high", 0),
                summary.get("medium", 0),
                summary.get("low", 0),
                summary.get("agents_reviewed", 0),
                json.dumps(results, default=str),
                report_path,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_reviews(limit: int = 50) -> list[dict]:
    """
    Return the most recent reviews, newest first.

    Each dict contains all scalar columns (no results_json for efficiency).
    """
    conn = _get_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, owner, repo, pull_request, overall_score, recommendation,
                   critical, high, medium, low, agents_reviewed,
                   report_path, created_at
            FROM reviews
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_review(review_id: int) -> dict | None:
    """
    Return a single review by ID, including the full results_json.

    Returns None if the ID does not exist.
    """
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM reviews WHERE id = ?", (review_id,)
        ).fetchone()
        if row is None:
            return None
        result = dict(row)
        # Deserialise the stored JSON back into a Python list
        if result.get("results_json"):
            result["results_json"] = json.loads(result["results_json"])
        return result
    finally:
        conn.close()
