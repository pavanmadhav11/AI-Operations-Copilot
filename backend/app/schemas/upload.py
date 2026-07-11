from datetime import datetime

from pydantic import BaseModel


class UploadedFileResponse(BaseModel):
    id: int
    user_id: int
    session_id: int
    filename: str
    file_type: str
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True