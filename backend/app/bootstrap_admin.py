import argparse

from sqlalchemy import func

from app.db.database import SessionLocal
from app.models.user import User


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    db = SessionLocal()
    try:
        user = db.query(User).filter(func.lower(User.email) == args.email.lower()).first()
        if user is None:
            raise SystemExit("No registered account matches that email.")
        user.role = "admin"
        db.commit()
        print(f"Admin role assigned to {user.email}.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
