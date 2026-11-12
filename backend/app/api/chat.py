from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse,
)

from app.services.chat_service import (
    generate_ai_response,
    get_chat_history,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ai_response = generate_ai_response(
        db=db,
        session_id=request.session_id,
        message=request.message,
        user_id=current_user.id,
    )

    return ChatResponse(
        response=ai_response,
    )


@router.get("/{session_id}/history")
def history(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_chat_history(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )
