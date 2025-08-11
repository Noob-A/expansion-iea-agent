from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel


class SignalCreate(BaseModel):
    channel_id: int
    message_id: int
    message_date: datetime
    symbol: str
    side: Literal["long", "short"]
    leverage: Optional[int] = None
    stop_loss: Optional[List[float]] = None
    take_profits: List[float]
    original_text: str
