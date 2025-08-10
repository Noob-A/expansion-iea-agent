from __future__ import annotations

"""Stub implementation of the information exploration step.

The production project relies on LLMs and rich prompting.  For our unit
tests we simply retrieve related documents from memory and return them as
context while also storing a short summary back to memory.
"""

from typing import Dict, Any
from ..memory import search_knowledge, upsert_knowledge


def run_info_exploration(question: str) -> Dict[str, Any]:
    docs = search_knowledge(question, k=5)
    summary = "\n".join(d.page_content for d in docs)
    if summary:
        upsert_knowledge(summary[:4000], {"source": "info_exploration", "query": question})
    return {"question": question, "results": [d.page_content for d in docs]}

__all__ = ["run_info_exploration"]
