from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.services.notification_service import get_notifications, mark_notification_read


router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
def list_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_notifications(db, current_user.id, current_user.role)


@router.post("/{notification_id}/read")
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return mark_notification_read(db, notification_id, current_user.id)
