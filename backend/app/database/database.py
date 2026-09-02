"""
AutoSecAI — Database Module
============================
Provides persistence for review history.
Automatically uses PostgreSQL if DATABASE_URL is set in environment,
otherwise defaults to local SQLite.
"""

import json
import os
import sqlite3
from datetime import datetime, timezone

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DATA_DIR = os.path.join(_BASE_DIR, "data")
_DB_PATH = os.path.join(_DATA_DIR, "autosecai.db")

DATABASE_URL = os.getenv("DATABASE_URL")
IS_POSTGRES = DATABASE_URL and DATABASE_URL.startswith("postgres")

if IS_POSTGRES:
    import psycopg2
    from psycopg2.extras import DictCursor

def _get_connection():
    if IS_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        os.makedirs(_DATA_DIR, exist_ok=True)
        conn = sqlite3.connect(_DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def _execute(conn, query, params=(), commit=False):
    # PostgreSQL uses %s for params, SQLite uses ?
    if IS_POSTGRES:
        query = query.replace("?", "%s")
        # For Postgres we need RETURNING id to get the last inserted id easily if needed,
        # but here we'll just handle it dynamically if we can.
        cursor = conn.cursor(cursor_factory=DictCursor)
    else:
        cursor = conn.cursor()
        
    cursor.execute(query, params)
    if commit:
        conn.commit()
    return cursor

def init_db() -> None:
    conn = _get_connection()
    try:
        pk_def = "SERIAL PRIMARY KEY" if IS_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"
        
        # 1. Create users table
        query_users = f"""
            CREATE TABLE IF NOT EXISTS users (
                id              {pk_def},
                github_id       VARCHAR(255) UNIQUE NOT NULL,
                username        VARCHAR(255) NOT NULL,
                github_token    VARCHAR(500),
                created_at      VARCHAR(100) NOT NULL
            )
        """
        _execute(conn, query_users, commit=True)

        # 2. Create reviews table with user_id
        query_reviews = f"""
            CREATE TABLE IF NOT EXISTS reviews (
                id              {pk_def},
                user_id         INTEGER,
                owner           VARCHAR(255) NOT NULL,
                repo            VARCHAR(255) NOT NULL,
                pull_request    INTEGER NOT NULL,
                overall_score   VARCHAR(50),
                recommendation  VARCHAR(100),
                critical        INTEGER DEFAULT 0,
                high            INTEGER DEFAULT 0,
                medium          INTEGER DEFAULT 0,
                low             INTEGER DEFAULT 0,
                agents_reviewed INTEGER DEFAULT 0,
                results_json    TEXT,
                report_path     TEXT,
                created_at      VARCHAR(100) NOT NULL
            )
        """
        _execute(conn, query_reviews, commit=True)
        
        # Try to alter existing reviews table to add user_id (ignore if it already exists)
        try:
            _execute(conn, "ALTER TABLE reviews ADD COLUMN user_id INTEGER", commit=True)
        except Exception:
            pass # Column likely already exists
            
    finally:
        conn.close()

def upsert_user(github_id: str, username: str, github_token: str | None = None) -> int:
    """
    Upsert user by github_id and return user ID.
    """
    conn = _get_connection()
    try:
        created_at = datetime.now(timezone.utc).isoformat()
        cursor = _execute(conn, "SELECT id FROM users WHERE github_id = ?", (github_id,))
        row = cursor.fetchone()
        if row:
            user_id = row[0] if isinstance(row, (tuple, list)) else row["id"]
            _execute(
                conn,
                "UPDATE users SET username = ?, github_token = ? WHERE id = ?",
                (username, github_token, user_id),
                commit=True
            )
            return user_id
        else:
            query = "INSERT INTO users (github_id, username, github_token, created_at) VALUES (?, ?, ?, ?)"
            if IS_POSTGRES:
                query = query.replace("?", "%s") + " RETURNING id"
                c = conn.cursor()
                c.execute(query, (github_id, username, github_token, created_at))
                user_id = c.fetchone()[0]
                conn.commit()
                return user_id
            else:
                c = _execute(conn, query, (github_id, username, github_token, created_at), commit=True)
                return c.lastrowid
    finally:
        conn.close()

def save_review(owner: str, repo: str, pull_request: int, summary: dict, results: list, report_path: str, user_id: int | None = None) -> int:
    conn = _get_connection()
    try:
        created_at = datetime.now(timezone.utc).isoformat()
        params = (
            user_id, owner, repo, pull_request, summary.get("overall_score", "N/A"),
            summary.get("recommendation", "N/A"), summary.get("critical", 0),
            summary.get("high", 0), summary.get("medium", 0), summary.get("low", 0),
            summary.get("agents_reviewed", 0), json.dumps(results, default=str),
            report_path, created_at
        )
        
        query = """
            INSERT INTO reviews
                (user_id, owner, repo, pull_request, overall_score, recommendation,
                 critical, high, medium, low, agents_reviewed,
                 results_json, report_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        if IS_POSTGRES:
            query = query.replace("?", "%s") + " RETURNING id"
            cursor = conn.cursor()
            cursor.execute(query, params)
            last_id = cursor.fetchone()[0]
            conn.commit()
            return last_id
        else:
            cursor = _execute(conn, query, params, commit=True)
            return cursor.lastrowid
    finally:
        conn.close()

def get_reviews(user_id: int | None = None, limit: int = 50) -> list[dict]:
    conn = _get_connection()
    try:
        if user_id is not None:
            query = """
                SELECT id, user_id, owner, repo, pull_request, overall_score, recommendation,
                       critical, high, medium, low, agents_reviewed,
                       report_path, created_at
                FROM reviews
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
            """
            cursor = _execute(conn, query, (user_id, limit))
        else:
            query = """
                SELECT id, user_id, owner, repo, pull_request, overall_score, recommendation,
                       critical, high, medium, low, agents_reviewed,
                       report_path, created_at
                FROM reviews
                ORDER BY id DESC
                LIMIT ?
            """
            cursor = _execute(conn, query, (limit,))
            
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_review(review_id: int) -> dict | None:
    conn = _get_connection()
    try:
        cursor = _execute(conn, "SELECT * FROM reviews WHERE id = ?", (review_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        result = dict(row)
        if result.get("results_json"):
            result["results_json"] = json.loads(result["results_json"])
        return result
    finally:
        conn.close()
