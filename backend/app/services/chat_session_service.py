from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession


def create_session(
    db: Session,
    user_id: int,
    title: str = "New Chat",
):
    session = ChatSession(
        user_id=user_id,
        title=title,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_sessions(
    db: Session,
    user_id: int,
):
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )


def get_session(
    db: Session,
    session_id: int,
    user_id: int,
):
    return (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id,
        )
        .first()
    )


def delete_session(
    db: Session,
    session: ChatSession,
):
    db.delete(session)
    db.commit()