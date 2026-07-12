from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.chat import ChatMessage
from app.models.uploaded_file import UploadedFile


def get_dashboard_stats(db: Session):
    users = db.query(func.count(User.id)).scalar() or 0

    documents = db.query(func.count(UploadedFile.id)).scalar() or 0

    ai_requests = (
        db.query(func.count(ChatMessage.id))
        .filter(ChatMessage.role == "user")
        .scalar()
        or 0
    )

    total_storage = (
        db.query(func.sum(func.length(UploadedFile.extracted_text)))
        .scalar()
        or 0
    )

    storage = round(total_storage / (1024 * 1024), 2)

    return {
        "users": users,
        "documents": documents,
        "aiRequests": ai_requests,
        "storage": f"{storage} MB",
    }


def get_recent_documents(db: Session):
    docs = (
        db.query(UploadedFile)
        .order_by(UploadedFile.uploaded_at.desc())
        .limit(5)
        .all()
    )

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
        }
        for doc in docs
    ]


def get_recent_activity(db: Session):
    chats = (
        db.query(ChatMessage)
        .order_by(ChatMessage.created_at.desc())
        .limit(5)
        .all()
    )

    return [
        {
            "text": f"{msg.role.title()} message"
        }
        for msg in chats
    ]


def get_activity_chart(db: Session):
    data = (
        db.query(
            func.date(ChatMessage.created_at),
            func.count(ChatMessage.id),
        )
        .group_by(func.date(ChatMessage.created_at))
        .order_by(func.date(ChatMessage.created_at))
        .all()
    )

    return [
        {
            "date": str(day),
            "requests": count,
        }
        for day, count in data
    ]