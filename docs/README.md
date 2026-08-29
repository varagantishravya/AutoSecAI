# AutoSecAI

**A Multi-Agent LLM Framework for Intelligent Pull Request Review**

AutoSecAI automatically reviews GitHub Pull Requests using six specialised AI agents that analyse Security, Code Quality, Performance, Testing, Documentation, and produce an overall Summary — all powered by LLMs.

---

## Features

- **Multi-Agent Architecture** — Six independent AI agents analyse different aspects of your code changes
- **Parallel Execution** — All specialist agents run concurrently for fast reviews
- **GitHub Integration** — Connects directly to your repositories via the GitHub API
- **Downloadable Reports** — Generates comprehensive Markdown reports for every review
- **Review History** — Persists past reviews in a local SQLite database
- **Severity Scoring** — Aggregates findings into Critical / High / Medium / Low counts with an overall 0-10 score
- **Modern Web UI** — React dashboard for repository selection, analysis, and history browsing

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      React Frontend                          │
│   Navbar │ Hero │ Analysis │ Dashboard │ Footer               │
└─────────────────────────┬────────────────────────────────────┘
                          │  HTTP (axios)
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Coordinator Agent                        │    │
│  │                                                       │    │
│  │  ┌─────────┐ ┌────────┐ ┌───────┐ ┌──────┐ ┌─────┐  │    │
│  │  │Security │ │Quality │ │Perf.  │ │Test  │ │Docs │  │    │
│  │  │ Agent   │ │ Agent  │ │Agent  │ │Agent │ │Agent│  │    │
│  │  └────┬────┘ └───┬────┘ └──┬────┘ └──┬───┘ └──┬──┘  │    │
│  │       └──────────┴─────────┴─────────┴────────┘      │    │
│  │                          │                            │    │
│  │                   Summary Agent                       │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  GitHub Module │ Database │ Report Generator │ LLM Client    │
└──────────────────────────────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        GitHub API              Groq API (LLM)
```

---

## Tech Stack

| Layer    | Technology                             |
|----------|----------------------------------------|
| Frontend | React 19, Vite, Axios, Recharts        |
| Backend  | Python, FastAPI, Uvicorn               |
| LLM      | Groq API (LLaMA 3.1 8B Instant)       |
| GitHub   | PyGithub, GitHub REST API              |
| Database | SQLite (built-in `sqlite3`)            |
| Styling  | Vanilla CSS with CSS custom properties |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [GitHub Personal Access Token](https://github.com/settings/tokens)
- A [Groq API Key](https://console.groq.com/keys)

### 1. Clone & Setup

```bash
git clone https://github.com/<your-username>/AutoSecAI.git
cd AutoSecAI

# One-click setup (Windows)
scripts\setup.bat
```

Or manually:

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Configure Environment

Create `backend/.env`:

```env
GITHUB_TOKEN=ghp_your_github_token_here
GROQ_API_KEY=gsk_your_groq_key_here
```

### 3. Run

```bash
# Terminal 1 — Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## API Reference

| Method | Endpoint                   | Description                          |
|--------|----------------------------|--------------------------------------|
| GET    | `/`                        | Welcome message                      |
| GET    | `/health`                  | Health check                         |
| GET    | `/repositories`            | List user's GitHub repositories      |
| GET    | `/pull-requests`           | List open PRs (query: owner, repo)   |
| GET    | `/changed-files`           | List changed files in a PR           |
| POST   | `/review`                  | Run multi-agent PR review            |
| GET    | `/download-report`         | Download Markdown report             |
| GET    | `/review-history`          | List past reviews                    |
| GET    | `/review-history/{id}`     | Get a single review with full results|

### POST `/review` — Request Body

```json
{
  "owner": "octocat",
  "repository": "hello-world",
  "pull_request": 42
}
```

---

## AI Agents

| Agent               | Focus Area                                      |
|---------------------|------------------------------------------------|
| **Security Agent**       | Vulnerabilities, hardcoded secrets, injection risks |
| **Code Quality Agent**   | Naming, structure, complexity, best practices       |
| **Performance Agent**    | Loops, DB calls, blocking I/O, algorithmic issues   |
| **Testing Agent**        | Missing tests, edge cases, test coverage gaps       |
| **Documentation Agent**  | Missing docstrings, type hints, inline comments     |
| **Summary Agent**        | Aggregates all findings into a final verdict        |

---

## Project Structure

```
AutoSecAI/
├── backend/
│   ├── app/
│   │   ├── agents/          # 6 AI agent modules
│   │   ├── api/             # FastAPI route definitions
│   │   ├── coordinator/     # Orchestrates agents
│   │   ├── database/        # SQLite persistence
│   │   ├── github/          # GitHub API integration
│   │   ├── llm/             # LLM client (Groq)
│   │   ├── models/          # Pydantic models
│   │   ├── rag/             # RAG knowledge base (stub)
│   │   ├── reports/         # Markdown report generator
│   │   ├── services/        # Standalone service wrappers
│   │   ├── utils/           # Logger, timing utilities
│   │   └── main.py          # FastAPI app entrypoint
│   ├── data/                # SQLite database (auto-created)
│   ├── logs/                # Log files (auto-created)
│   ├── reports/             # Generated reports
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React UI components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API client (axios)
│   │   └── styles/          # CSS design tokens
│   └── package.json
├── docs/                    # Documentation
└── scripts/                 # Setup & launch scripts
```

---

## License

This project is for educational and research purposes.
