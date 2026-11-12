from fastapi import HTTPException
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.purchase_order import PurchaseOrder
from app.models.recommendation_outcome import RecommendationOutcome
from app.models.stock_movement import StockMovement


def record_recommendation_feedback(db: Session, user_id: int, feedback):
    if feedback.recommendation_type not in {"transfer", "reorder"}:
        raise HTTPException(status_code=400, detail="Recommendation type must be transfer or reorder.")
    inventory = db.query(Inventory).filter(Inventory.id == feedback.inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found.")
    outcome = RecommendationOutcome(
        user_id=user_id,
        inventory_id=feedback.inventory_id,
        recommendation_type=feedback.recommendation_type,
        recommended_quantity=feedback.recommended_quantity,
        actual_quantity=None,
        accepted=feedback.accepted,
        note=feedback.note,
    )
    db.add(outcome)
    db.commit()
    return {"id": outcome.id, "accepted": outcome.accepted}


def get_recommendation_metrics(db: Session, user_id: int, role: str):
    outcome_query = db.query(RecommendationOutcome)
    movement_query = db.query(StockMovement)
    order_query = db.query(PurchaseOrder).filter(PurchaseOrder.status == "draft")
    if role != "admin":
        outcome_query = outcome_query.filter(RecommendationOutcome.user_id == user_id)
        movement_query = movement_query.filter(StockMovement.user_id == user_id)
        order_query = order_query.filter(PurchaseOrder.user_id == user_id)
    outcome_stats = outcome_query.with_entities(
        func.count(RecommendationOutcome.id),
        func.sum(case((RecommendationOutcome.accepted.is_(True), 1), else_=0)),
        func.sum(case((RecommendationOutcome.accepted.is_(False), 1), else_=0)),
    ).one()
    by_type = outcome_query.with_entities(
        RecommendationOutcome.recommendation_type,
        func.count(RecommendationOutcome.id),
        func.sum(case((RecommendationOutcome.accepted.is_(True), 1), else_=0)),
    ).group_by(RecommendationOutcome.recommendation_type).all()
    expired_units = movement_query.with_entities(
        func.sum(-StockMovement.quantity_change)
    ).filter(StockMovement.movement_type == "expiry_writeoff").scalar() or 0
    draft_count = order_query.count()
    total = outcome_stats[0] or 0
    accepted = int(outcome_stats[1] or 0)
    rejected = int(outcome_stats[2] or 0)
    return {
        "total_feedback": total,
        "accepted": accepted,
        "rejected": rejected,
        "acceptance_rate": round(accepted * 100 / total, 1) if total else 0,
        "purchase_order_drafts": draft_count,
        "expired_units_written_off": int(expired_units),
        "by_type": [
            {"type": item[0], "feedback_count": item[1], "accepted": int(item[2] or 0)}
            for item in by_type
        ],
    }
