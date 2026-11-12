from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.db.session import get_db
from app.schemas.procurement import PurchaseOrderDraftRequest
from app.services.procurement_service import create_purchase_order_draft, extract_purchase_quote, list_purchase_orders


router = APIRouter(prefix="/procurement", tags=["Procurement"])


@router.get("/orders")
def orders(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return list_purchase_orders(db, current_user.id, current_user.role)


@router.post("/quotes/{file_id}/extract")
def extract_quote(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return extract_purchase_quote(db, file_id, current_user.id)


@router.post("/quotes/{file_id}/draft")
def create_draft(
    file_id: int,
    request: PurchaseOrderDraftRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return create_purchase_order_draft(db, file_id, current_user.id, request)
