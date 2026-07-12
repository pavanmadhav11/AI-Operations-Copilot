from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.dependencies import (
    get_current_user,
)

from app.schemas.settings import (
    ProfileResponse,
    UpdateProfileRequest,
    ChangePasswordRequest,
)

from app.services.settings_service import (
    update_profile,
    change_password,
)

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get(
    "/profile",
    response_model=ProfileResponse,
)
def profile(
    current_user=Depends(get_current_user),
):
    return current_user


@router.put(
    "/profile",
    response_model=ProfileResponse,
)
def update(
    request: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_profile(
        db,
        current_user,
        request.name,
        request.email,
    )


@router.put("/password")
def password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return change_password(
            db,
            current_user,
            request.current_password,
            request.new_password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )