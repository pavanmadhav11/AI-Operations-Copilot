import os

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.chat import ChatMessage
from app.models.chat_session import ChatSession
from app.models.uploaded_file import UploadedFile


def get_dashboard_analytics(db: Session):
    users = db.query(User).count()

    sessions = db.query(ChatSession).count()

    ai_requests = (
        db.query(ChatMessage)
        .filter(ChatMessage.role == "user")
        .count()
    )

    documents = db.query(UploadedFile).count()

    pdfs = (
        db.query(UploadedFile)
        .filter(
            UploadedFile.file_type == "application/pdf"
        )
        .count()
    )

    excels = (
        db.query(UploadedFile)
        .filter(
            UploadedFile.file_type.in_(
                [
                    "application/vnd.ms-excel",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ]
            )
        )
        .count()
    )

    storage = 0

    for file in db.query(UploadedFile).all():
        if os.path.exists(file.file_path):
            storage += os.path.getsize(file.file_path)

    storage = round(storage / (1024 * 1024), 2)

    uploads_per_day = (
        db.query(
            func.date(UploadedFile.uploaded_at),
            func.count(UploadedFile.id),
        )
        .group_by(
            func.date(UploadedFile.uploaded_at)
        )
        .all()
    )

    chart = [
        {
            "date": str(day),
            "uploads": total,
        }
        for day, total in uploads_per_day
    ]

    return {
        "users": users,
        "sessions": sessions,
        "documents": documents,
        "pdfs": pdfs,
        "excels": excels,
        "ai_requests": ai_requests,
        "storage": f"{storage} MB",
        "chart": chart,
    }