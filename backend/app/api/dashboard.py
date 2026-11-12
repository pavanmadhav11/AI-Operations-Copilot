from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user

from app.services.dashboard_service import (
    get_dashboard_stats,
    get_recent_documents,
    get_recent_activity,
    get_activity_chart,
    get_low_stock_inventory,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_dashboard_stats(db, current_user.id, current_user.role)


@router.get("/low-stock")
def low_stock(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_low_stock_inventory(db)


@router.get("/activity")
def activity(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_activity_chart(db, current_user.id, current_user.role)


@router.get("/recent-activity")
def recent_activity(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_recent_activity(db, current_user.id, current_user.role)


@router.get("/recent-documents")
def recent_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_recent_documents(db, current_user.id, current_user.role)
