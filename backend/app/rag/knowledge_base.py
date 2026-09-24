"""
AutoSecAI — RAG Knowledge Base
================================
Provides a ChromaDB-backed document store for RAG-based context retrieval.

Usage:
    from app.rag.knowledge_base import KnowledgeBase

    kb = KnowledgeBase()
    kb.add_document("SQL injection occurs when ...", {"source": "owasp"})
    results = kb.search("SQL injection", top_k=3)
"""

from __future__ import annotations
import os

try:
    import chromadb
except Exception:
    chromadb = None

from typing import Any

# Store the Chroma DB inside backend/data/chroma
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_CHROMA_DIR = os.path.join(_BASE_DIR, "data", "chroma")

class KnowledgeBase:
    """
    ChromaDB-backed document store for RAG-based context retrieval (with fallback).
    """

    def __init__(self) -> None:
        self.client = None
        self.collection = None
        if chromadb is not None:
            try:
                os.makedirs(_CHROMA_DIR, exist_ok=True)
                self.client = chromadb.PersistentClient(path=_CHROMA_DIR)
                self.collection = self.client.get_or_create_collection(name="autosecai_knowledge")
                
                # Auto-seed OWASP security rules if empty
                if self.collection.count() == 0:
                    try:
                        from app.rag.seed_knowledge import seed_default_knowledge
                        seed_default_knowledge(self)
                    except Exception as e:
                        print(f"Notice: RAG auto-seeding skipped: {e}")
            except Exception as e:
                print(f"Notice: ChromaDB init skipped: {e}")


    # ── Public API ─────────────────────────────────────────────────────

    def add_document(self, text: str, metadata: dict[str, Any] | None = None) -> str:
        """
        Add a document and return its ID.

        Args:
            text:     The document content.
            metadata: Optional key-value metadata (e.g. source, category).

        Returns:
            The string ID of the newly added document.
        """
        import uuid
        doc_id = str(uuid.uuid4())
        
        if self.collection is not None:
            self.collection.add(
                documents=[text],
                metadatas=[metadata or {}],
                ids=[doc_id]
            )
        return doc_id

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        """
        Return the *top_k* most relevant documents for *query*.

        Each result is a dict with keys: ``text``, ``metadata``, ``score``.
        Results are sorted by descending relevance score.
        """
        if not query.strip() or self.collection is None:
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        output = []
        if results and results["documents"] and len(results["documents"][0]) > 0:
            docs = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0] * len(docs)
            
            for i in range(len(docs)):
                output.append({
                    "text": docs[i],
                    "metadata": metadatas[i],
                    "score": round(distances[i], 4), # Note: Chroma returns distance. Smaller is better.
                })
                
        return output

    @property
    def size(self) -> int:
        """Number of documents currently stored."""
        return self.collection.count() if self.collection is not None else 0
