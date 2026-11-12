from datetime import datetime
import json

from pydantic import BaseModel, field_validator


class UploadedFileResponse(BaseModel):
    id: int
    user_id: int
    session_id: int | None = None

    filename: str
    file_type: str

    summary: str | None = None
    workbook_json: str | None = None

    uploaded_at: datetime

    class Config:
        from_attributes = True

    @field_validator("workbook_json")
    @classmethod
    def remove_internal_workbook_path(cls, value):
        if not value:
            return value
        try:
            workbook = json.loads(value)
        except json.JSONDecodeError:
            return None
        if not isinstance(workbook, dict):
            return None
        workbook.pop("workbook", None)
        return json.dumps(workbook, default=str)
