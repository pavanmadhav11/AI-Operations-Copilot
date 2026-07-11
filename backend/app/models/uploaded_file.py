from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

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

    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id"),
        nullable=False,
    )

    filename = Column(
        String(255),
        nullable=False,
    )

    file_type = Column(
        String(100),
    )

    file_path = Column(
        String(500),
        nullable=False,
    )

    extracted_text = Column(Text)

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    session = relationship(
        "ChatSession",
        back_populates="files",
    )