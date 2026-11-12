from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db

from app.schemas.chat_session import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatSessionUpdate,
)

from app.services.chat_session_service import (
    create_session,
    get_sessions,
    get_session,
    delete_session,
    rename_session,
)

router = APIRouter(
    prefix="/chat/sessions",
    tags=["Chat Sessions"],
)


@router.post(
    "",
    response_model=ChatSessionResponse,
)
def create_new_session(
    request: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_session(
        db=db,
        user_id=current_user.id,
        title=request.title,
    )


@router.get(
    "",
    response_model=list[ChatSessionResponse],
)
def list_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_sessions(
        db=db,
        user_id=current_user.id,
    )


@router.delete("/{session_id}")
def remove_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    session = get_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    delete_session(
        db=db,
        session=session,
    )

    return {
        "message": "Session deleted"
    }


@router.patch("/{session_id}", response_model=ChatSessionResponse)
def rename_existing_session(
    session_id: int,
    request: ChatSessionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    session = get_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return rename_session(db, session, request.title)
