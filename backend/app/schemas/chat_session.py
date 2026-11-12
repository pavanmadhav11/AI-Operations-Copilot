from pydantic import BaseModel
from datetime import datetime


class ChatSessionCreate(BaseModel):
    title: str = "New Chat"


class ChatSessionUpdate(BaseModel):
    title: str


class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True
