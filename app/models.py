from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy import String, DateTime, Integer, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class TradeSide(str, Enum):
    long = "long"
    short = "short"


class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    signals: Mapped[List["Signal"]] = relationship(back_populates="channel")


class Signal(Base):
    __tablename__ = "signals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))
    message_id: Mapped[int] = mapped_column(Integer)
    message_date: Mapped[datetime] = mapped_column(DateTime)
    symbol: Mapped[str] = mapped_column(String)
    side: Mapped[TradeSide] = mapped_column(SAEnum(TradeSide))
    leverage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    stop_loss: Mapped[Optional[List[float]]] = mapped_column(JSON, nullable=True)
    take_profits: Mapped[List[float]] = mapped_column(JSON)
    original_text: Mapped[str] = mapped_column(String)
    channel: Mapped[Channel] = relationship(back_populates="signals")
