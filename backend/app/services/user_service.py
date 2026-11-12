from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.hashing import (
    hash_password,
    verify_password,
)
from app.auth.jwt import create_access_token


def create_user(db: Session, user):
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="employee",
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db: Session, user):
    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not db_user:
        return None

    if not verify_password(
        user.password,
        db_user.hashed_password,
    ):
        return None

    token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
