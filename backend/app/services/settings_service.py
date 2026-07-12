from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.hashing import (
    verify_password,
    hash_password,
)


def update_profile(
    db: Session,
    user: User,
    name: str,
    email: str,
):
    user.name = name
    user.email = email

    db.commit()
    db.refresh(user)

    return user


def change_password(
    db: Session,
    user: User,
    current_password: str,
    new_password: str,
):
    if not verify_password(
        current_password,
        user.hashed_password,
    ):
        raise ValueError(
            "Current password is incorrect."
        )

    user.hashed_password = hash_password(
        new_password
    )

    db.commit()

    return {
        "message": "Password updated successfully."
    }