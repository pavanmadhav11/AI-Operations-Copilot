from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.db.session import get_db
from app.schemas.inventory import RecommendationFeedback
from app.services.recommendation_service import get_recommendation_metrics, record_recommendation_feedback


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/metrics")
def metrics(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return get_recommendation_metrics(db, current_user.id, current_user.role)


@router.post("/feedback")
def feedback(
    request: RecommendationFeedback,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return record_recommendation_feedback(db, current_user.id, request)
