from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.analytics_service import (
    get_dashboard_analytics,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("")
def analytics(
    db: Session = Depends(get_db),
):
    return get_dashboard_analytics(db)