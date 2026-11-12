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
from app.auth.dependencies import require_roles
from app.models.user import User as UserModel
from app.schemas.user import UserRoleUpdate

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


@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    return db.query(UserModel).order_by(UserModel.id.asc()).all()


@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    request: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    if request.role not in {"admin", "manager", "employee"}:
        raise HTTPException(status_code=400, detail="Role must be admin, manager, or employee.")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if user.role == "admin" and request.role != "admin":
        admins = db.query(UserModel).filter(UserModel.role == "admin").count()
        if admins <= 1:
            raise HTTPException(status_code=400, detail="The last admin cannot be demoted.")

    user.role = request.role
    db.commit()
    db.refresh(user)
    return user
