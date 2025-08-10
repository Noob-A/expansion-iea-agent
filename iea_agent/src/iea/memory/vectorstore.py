from __future__ import annotations

"""Lightweight in-memory vector store used for tests.

This avoids heavy dependencies like Postgres/pgvector or Chroma.  The
implementation is intentionally simple: documents are embedded using a
bag-of-words representation and cosine similarity is used for search.
"""

from collections import Counter
from typing import Dict, List
import math

from .types import Document

class SimpleVectorStore:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.docs: List[Document] = []

    def add_documents(self, docs: List[Document]) -> None:
        self.docs.extend(docs)

    # --- internal helpers -------------------------------------------------
    @staticmethod
    def _embed(text: str) -> Counter:
        return Counter(text.lower().split())

    def _similarity(self, a: Counter, b: Counter) -> float:
        dot = sum(a[w] * b[w] for w in a)
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    # --- public API -------------------------------------------------------
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        q_vec = self._embed(query)
        scored = [
            (self._similarity(q_vec, self._embed(doc.page_content)), doc)
            for doc in self.docs
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:k]]

_STORES: Dict[str, SimpleVectorStore] = {}

def get_vectorstore(collection: str = "iea_memory") -> SimpleVectorStore:
    return _STORES.setdefault(collection, SimpleVectorStore(collection))

__all__ = ["get_vectorstore", "SimpleVectorStore"]
