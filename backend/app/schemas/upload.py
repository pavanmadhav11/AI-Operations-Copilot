from datetime import datetime
from pydantic import BaseModel


class UploadedFileResponse(BaseModel):
    id: int
    user_id: int
    session_id: int | None = None

    filename: str
    file_type: str
    file_path: str

    summary: str | None = None
    workbook_json: str | None = None

    uploaded_at: datetime

    class Config:
        from_attributes = True