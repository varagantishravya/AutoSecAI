# AutoSecAI — Architecture

This document describes the system architecture, data flow, and component responsibilities.

---

## System Overview

AutoSecAI is a **multi-agent LLM framework** that performs automated code review on GitHub Pull Requests. The system follows a **coordinator pattern** where a central orchestrator dispatches work to specialised AI agents running in parallel.

---

## Data Flow

```
User selects Repo + PR in the UI
            │
            ▼
    Frontend (React) ──POST /review──▶ FastAPI Backend
                                            │
                                            ▼
                                    CoordinatorAgent
                                            │
                        ┌───────────────────┼───────────────────┐
                        │                   │                   │
                        ▼                   ▼                   ▼
                 ┌──────────┐      ┌──────────┐       ┌──────────┐
                 │ Security │      │ Quality  │       │  Perf.   │
                 │  Agent   │      │  Agent   │       │  Agent   │
                 └────┬─────┘      └────┬─────┘       └────┬─────┘
                      │                 │                   │
                 ┌────┴────┐      ┌─────┴────┐              │
                 │ Testing │      │  Docs    │              │
                 │  Agent  │      │  Agent   │              │
                 └────┬────┘      └────┬─────┘              │
                      │                │                    │
                      └────────────────┴────────────────────┘
                                       │
                                       ▼
                                Summary Agent
                                       │
                          ┌────────────┼────────────┐
                          ▼            ▼            ▼
                     Save to DB   Generate     Return JSON
                     (SQLite)     Report (MD)   to Frontend
```

---

## Component Responsibilities

### Backend Components

| Component | Location | Responsibility |
|-----------|----------|----------------|
| **FastAPI App** | `app/main.py` | Application setup, CORS, middleware, DB init |
| **API Router** | `app/api/routes.py` | All HTTP endpoint definitions |
| **Coordinator** | `app/coordinator/coordinator.py` | Orchestrates agents, parses results, triggers report & DB save |
| **AI Agents** | `app/agents/*/analyzer.py` | Each agent sends a specialised prompt to the LLM and returns structured findings |
| **LLM Client** | `app/llm/client.py` | Wraps the Groq API (OpenAI-compatible) to provide a unified `chat()` interface |
| **GitHub Module** | `app/github/` | Fetches repositories, pull requests, and file diffs via PyGithub |
| **Database** | `app/database/database.py` | SQLite CRUD for review history |
| **Report Generator** | `app/reports/report_generator.py` | Writes a comprehensive Markdown report to disk |
| **RAG Knowledge Base** | `app/rag/knowledge_base.py` | In-memory TF-IDF document search (stub for future vector DB) |
| **Utils** | `app/utils/` | Structured logger with file output, `@timed` decorator |

### Frontend Components

| Component | Location | Responsibility |
|-----------|----------|----------------|
| **Navbar** | `components/Navbar/` | Top navigation bar with branding and links |
| **Hero** | `components/Hero/` | Landing section with CTA to start analysis |
| **Analysis** | `components/Analysis/` | Repository/PR selection → review trigger → results display |
| **Dashboard** | `components/Dashboard/` | Review history table with stats |
| **Footer** | `components/Layout/Footer` | Page footer with project info |
| **StatusBadge** | `components/common/StatusBadge` | Colour-coded severity indicator |
| **ScoreGauge** | `components/common/ScoreGauge` | Animated circular score visualisation |

---

## Agent Execution Model

1. The **Coordinator** receives the PR number and fetches all changed files from GitHub.
2. Patches are classified by file extension and content keywords, then dispatched to the appropriate agents.
3. All **5 specialist agents** execute in parallel using `ThreadPoolExecutor(max_workers=5)`.
4. Once all 5 complete, their results are passed to the **Summary Agent** which produces a consolidated verdict.
5. The coordinator parses the summary (scores, severity counts, recommendation) via regex.
6. Results are saved to SQLite, a Markdown report is written to disk, and the full JSON is returned to the frontend.

---

## Database Schema

```sql
CREATE TABLE reviews (
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
    results_json    TEXT,          -- full agent results as JSON string
    report_path     TEXT,          -- filesystem path to the .md report
    created_at      TEXT NOT NULL  -- ISO 8601 UTC timestamp
);
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Groq instead of local Ollama** | Much faster inference; free tier is sufficient for development |
| **ThreadPoolExecutor for agents** | Simple, built-in parallelism; no need for Celery/Redis at this scale |
| **SQLite for persistence** | Zero-config, single-file database; perfect for a solo/small-team tool |
| **Regex-based summary parsing** | Avoids additional LLM calls; reliable enough for structured output |
| **RAG as a stub** | Provides a clear interface without requiring a vector DB dependency |
