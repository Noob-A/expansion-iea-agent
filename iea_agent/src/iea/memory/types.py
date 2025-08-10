from __future__ import annotations

"""Shared data structures for the memory subsystem."""
from dataclasses import dataclass, field

@dataclass
class Document:
    page_content: str
    metadata: dict = field(default_factory=dict)

__all__ = ["Document"]
