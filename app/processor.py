from __future__ import annotations
from .llm import LLMClient


class Processor:
    """Placeholder processor handling parsed signals."""

    def __init__(self, llm: LLMClient, concurrency: int = 1):
        self.llm = llm
        self.concurrency = concurrency

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass
