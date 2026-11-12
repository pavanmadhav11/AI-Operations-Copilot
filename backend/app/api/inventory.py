from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.schemas.inventory import InventoryCreate, StockBatchCreate, TransferPreviewRequest, WarehouseCreate
from app.services.inventory_service import add_inventory_item, add_warehouse, get_inventory, get_warehouses
from app.services.stock_action_service import (
    confirm_stock_action,
    create_transfer_preview,
    get_stock_actions,
    get_stock_movements,
    reject_stock_action,
)
from app.services.stock_batch_service import add_stock_batch, get_expiring_batches, write_off_expired_batch


router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("")
def list_inventory(
    limit: int | None = Query(default=None, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_inventory(db, limit, offset)


@router.get("/warehouses")
def list_warehouses(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return get_warehouses(db)


@router.post("/warehouses")
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return add_warehouse(db, warehouse)


@router.post("")
def create_inventory_item(
    item: InventoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return add_inventory_item(db, item, current_user.id)


@router.get("/movements")
def list_stock_movements(
    limit: int = Query(default=25, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_stock_movements(db, limit, offset)


@router.get("/actions")
def list_stock_actions(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return get_stock_actions(db, current_user.id, current_user.role)


@router.post("/actions/{action_id}/confirm")
def confirm_action(
    action_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return confirm_stock_action(db, action_id, current_user.id, current_user.role)


@router.post("/actions/{action_id}/reject")
def reject_action(
    action_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return reject_stock_action(db, action_id, current_user.id, current_user.role)


@router.post("/transfers/preview")
def preview_transfer(
    request: TransferPreviewRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return create_transfer_preview(
        db,
        current_user.id,
        f"Transfer {request.quantity} units from inventory {request.source_inventory_id} to warehouse {request.destination_warehouse_id}",
        request.source_inventory_id,
        request.destination_warehouse_id,
        request.quantity,
        request.recommendation_inventory_id,
        request.recommended_quantity,
    )


@router.get("/batches/expiring")
def list_expiring_batches(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_expiring_batches(db, days)


@router.post("/batches")
def create_batch(
    batch: StockBatchCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return add_stock_batch(db, batch, current_user.id)


@router.post("/batches/{batch_id}/write-off")
def write_off_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return write_off_expired_batch(db, batch_id, current_user.id)
