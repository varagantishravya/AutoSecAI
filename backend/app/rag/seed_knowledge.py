"""
AutoSecAI — RAG Knowledge Base Seeder
======================================
Populates ChromaDB with OWASP Top 10 guidelines, CWE vulnerability rules,
and code quality best practices for multi-agent RAG context retrieval.
"""

OWASP_SECURITY_RULES = [
    {
        "text": (
            "OWASP A01:2021 — Broken Access Control. Ensure user inputs and IDs in URLs or requests "
            "are validated against session access controls (IDOR prevention). Always enforce authorization "
            "checks at the controller/route level."
        ),
        "metadata": {"category": "security", "source": "owasp_a01"}
    },
    {
        "text": (
            "OWASP A02:2021 — Cryptographic Failures. Avoid weak hashing algorithms like MD5 or SHA1 for passwords. "
            "Use Argon2, bcrypt, or PBKDF2. Never log plaintext passwords or sensitive tokens. Ensure TLS 1.3 for network requests."
        ),
        "metadata": {"category": "security", "source": "owasp_a02"}
    },
    {
        "text": (
            "OWASP A03:2021 — Injection (SQLi, Command Injection). Never concatenate raw user input into SQL queries or system commands. "
            "Use parameterized queries / prepared statements (ORM) for SQL. Use shlex or array-based subprocess execution for shell commands."
        ),
        "metadata": {"category": "security", "source": "owasp_a03"}
    },
    {
        "text": (
            "OWASP A04:2021 — Insecure Design. Validate all user inputs against strict schemas (Pydantic / Zod). "
            "Implement rate limiting on authentication and API routes to prevent brute-force attacks."
        ),
        "metadata": {"category": "security", "source": "owasp_a04"}
    },
    {
        "text": (
            "OWASP A05:2021 — Security Misconfiguration. Remove debug flags (e.g. DEBUG=True) in production environments. "
            "Restrict CORS origins to explicitly allowed domains. Never expose verbose stack traces to API consumers."
        ),
        "metadata": {"category": "security", "source": "owasp_a05"}
    },
    {
        "text": (
            "OWASP A07:2021 — Identification and Authentication Failures. Prevent hardcoded API keys, JWT secrets, "
            "or passwords in code repositories. Load secrets from environment variables or secure key vaults."
        ),
        "metadata": {"category": "security", "source": "owasp_a07"}
    },
    {
        "text": (
            "OWASP A10:2021 — Server-Side Request Forgery (SSRF). Validate and sanitize destination URLs before making backend HTTP requests. "
            "Block requests targeting local IP ranges (127.0.0.1, 10.0.0.0/8, 169.254.169.254)."
        ),
        "metadata": {"category": "security", "source": "owasp_a10"}
    },
    {
        "text": (
            "Performance Best Practice: Avoid O(N^2) nested loops over large datasets or remote calls. "
            "Batch database operations (bulk insert/update) and utilize async/await or connection pooling for I/O operations."
        ),
        "metadata": {"category": "performance", "source": "perf_best_practices"}
    }
]


def seed_default_knowledge(kb) -> int:
    """
    Seed the knowledge base if it is currently empty.
    Returns the number of seeded documents.
    """
    if kb.size > 0:
        return 0

    count = 0
    for rule in OWASP_SECURITY_RULES:
        kb.add_document(rule["text"], rule["metadata"])
        count += 1

    print(f"Successfully seeded RAG Knowledge Base with {count} OWASP security rules.")
    return count
