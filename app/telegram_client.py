from __future__ import annotations
from .processor import Processor


class TelegramListener:
    """Placeholder Telegram listener."""

    def __init__(self, processor: Processor):
        self.processor = processor

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass
