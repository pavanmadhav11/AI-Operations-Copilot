from sqlalchemy.orm import Session

from app.ai.llm import ask_llm
from app.ai.prompts import SYSTEM_PROMPT

from app.models.chat import ChatMessage
from app.models.chat_session import ChatSession

from app.services.upload_service import get_session_files


def save_message(
    db: Session,
    session_id: int,
    role: str,
    message: str,
):
    chat = ChatMessage(
        session_id=session_id,
        role=role,
        message=message,
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chat_history(
    db: Session,
    session_id: int,
):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )


def build_messages(
    history,
    current_message,
    document_text=None,
):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # Add uploaded documents as context
    if document_text:
        messages.append(
            {
                "role": "system",
                "content": f"""
You are an AI Operations Copilot.

The user has uploaded one or more documents.

Use the document contents to answer the user's questions.

If the answer is not available in the uploaded documents,
clearly say so.

Uploaded Documents:

{document_text[:12000]}
""",
            }
        )

    # Previous chat history
    for msg in history:
        messages.append(
            {
                "role": msg.role,
                "content": msg.message,
            }
        )

    # Current user message
    messages.append(
        {
            "role": "user",
            "content": current_message,
        }
    )

    return messages


def generate_ai_response(
    db: Session,
    session_id: int,
    message: str,
):
    # Load previous chat
    history = get_chat_history(
        db=db,
        session_id=session_id,
    )

    # Verify session exists
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    document_text = ""

    # Load all uploaded documents for this session
    if session:
        uploaded_files = get_session_files(
            db=db,
            session_id=session_id,
        )

        if uploaded_files:
            document_text = "\n\n".join(
                file.extracted_text or ""
                for file in uploaded_files
            )

    # Build LLM prompt
    messages = build_messages(
        history=history,
        current_message=message,
        document_text=document_text,
    )

    # Get AI response
    ai_response = ask_llm(messages)

    # Save user message
    save_message(
        db=db,
        session_id=session_id,
        role="user",
        message=message,
    )

    # Save AI response
    save_message(
        db=db,
        session_id=session_id,
        role="assistant",
        message=ai_response,
    )

    return ai_response