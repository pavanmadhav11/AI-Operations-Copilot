from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    title = Column(
        String(255),
        default="New Chat",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete",
    )

    files = relationship(
        "UploadedFile",
        back_populates="session",
        cascade="all, delete",
    )