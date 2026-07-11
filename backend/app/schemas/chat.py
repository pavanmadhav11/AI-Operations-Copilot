from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    session_id: int
    message: str


class ChatResponse(BaseModel):
    response: str


class ChatHistoryResponse(BaseModel):
    id: int
    session_id: int
    role: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True