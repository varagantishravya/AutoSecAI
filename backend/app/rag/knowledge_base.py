"""
AutoSecAI — RAG Knowledge Base (Lightweight Stub)
===================================================
Provides a simple in-memory document store with TF-IDF keyword search.

This module is intentionally lightweight and dependency-free so the project
can run without a vector database.  When you're ready to scale up, swap
the internals for ChromaDB, FAISS + sentence-transformers, or similar.

Usage:
    from app.rag.knowledge_base import KnowledgeBase

    kb = KnowledgeBase()
    kb.add_document("SQL injection occurs when ...", {"source": "owasp"})
    results = kb.search("SQL injection", top_k=3)

Upgrading to a real vector store:
    1. Install a vector DB:  pip install chromadb
    2. Replace `_index` with a ChromaDB collection.
    3. Replace `search()` with an embedding-based similarity query.
    4. Optionally feed the search results into agent prompts for context.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """A single document stored in the knowledge base."""
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


class KnowledgeBase:
    """
    In-memory document store with TF-IDF keyword search.

    This is a zero-dependency placeholder.  It is *not* designed for
    production-scale datasets — use it for a few hundred security rules,
    coding guidelines, or best-practice snippets that can augment agent
    prompts.
    """

    def __init__(self) -> None:
        self._documents: list[Document] = []

    # ── Public API ─────────────────────────────────────────────────────

    def add_document(self, text: str, metadata: dict[str, Any] | None = None) -> int:
        """
        Add a document and return its index.

        Args:
            text:     The document content.
            metadata: Optional key-value metadata (e.g. source, category).

        Returns:
            The integer index of the newly added document.
        """
        doc = Document(text=text, metadata=metadata or {})
        self._documents.append(doc)
        return len(self._documents) - 1

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        """
        Return the *top_k* most relevant documents for *query*.

        Each result is a dict with keys: ``text``, ``metadata``, ``score``.
        Results are sorted by descending relevance score.
        """
        if not self._documents or not query.strip():
            return []

        query_terms = self._tokenise(query)
        if not query_terms:
            return []

        # Pre-compute IDF for query terms
        idf = self._compute_idf(query_terms)

        scored: list[tuple[float, int]] = []
        for idx, doc in enumerate(self._documents):
            score = self._tfidf_score(doc.text, query_terms, idf)
            if score > 0:
                scored.append((score, idx))

        scored.sort(key=lambda t: t[0], reverse=True)

        results = []
        for score, idx in scored[:top_k]:
            doc = self._documents[idx]
            results.append({
                "text": doc.text,
                "metadata": doc.metadata,
                "score": round(score, 4),
            })
        return results

    @property
    def size(self) -> int:
        """Number of documents currently stored."""
        return len(self._documents)

    # ── Private helpers ────────────────────────────────────────────────

    @staticmethod
    def _tokenise(text: str) -> list[str]:
        """Lowercase + split on non-alphanumeric characters."""
        return [t for t in re.split(r"\W+", text.lower()) if t]

    def _compute_idf(self, terms: list[str]) -> dict[str, float]:
        """Inverse document frequency for each term across the corpus."""
        n = len(self._documents)
        idf: dict[str, float] = {}
        for term in set(terms):
            doc_count = sum(
                1 for doc in self._documents if term in self._tokenise(doc.text)
            )
            # Smoothed IDF to avoid division by zero
            idf[term] = math.log((n + 1) / (doc_count + 1)) + 1
        return idf

    def _tfidf_score(
        self, text: str, query_terms: list[str], idf: dict[str, float]
    ) -> float:
        """Compute the TF-IDF cosine-ish relevance score for a document."""
        tokens = self._tokenise(text)
        if not tokens:
            return 0.0

        tf = Counter(tokens)
        max_tf = max(tf.values())

        score = 0.0
        for term in query_terms:
            term_tf = tf.get(term, 0) / max_tf  # normalised TF
            score += term_tf * idf.get(term, 0)
        return score
