from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)

from app.services.user_service import (
    create_user,
    login_user,
)

from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user)


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    token = login_user(db, user)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return token


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    return current_user