import json
from datetime import date, datetime, timezone

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.product import Product
from app.models.recommendation_outcome import RecommendationOutcome
from app.models.stock_action import StockAction
from app.models.stock_batch import StockBatch
from app.models.stock_movement import StockMovement
from app.models.user import User
from app.models.warehouse import Warehouse


def create_quantity_action(db: Session, user_id: int, request_text: str, sql: str, inventory_id: int, quantity: int):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found.")

    details = {
        "inventory_id": inventory.id,
        "quantity_before": inventory.quantity,
        "quantity_after": quantity,
    }
    product = db.query(Product).filter(Product.id == inventory.product_id).first()
    warehouse = db.query(Warehouse).filter(Warehouse.id == inventory.warehouse_id).first()
    action = StockAction(
        user_id=user_id,
        action_type="set_quantity",
        request_text=request_text,
        generated_sql=sql,
        details_json=json.dumps(details),
        status="pending",
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return {
        "action_id": action.id,
        "product_id": inventory.product_id,
        "product_name": product.name if product else "Unknown product",
        "warehouse_name": warehouse.name if warehouse else "Unknown warehouse",
        "inventory_id": inventory.id,
        "request_text": request_text,
        "quantity_before": inventory.quantity,
        "quantity_after": quantity,
        "status": action.status,
    }


def create_transfer_preview(db: Session, user_id: int, request_text: str, source_inventory_id: int, destination_warehouse_id: int, quantity: int, recommendation_inventory_id=None, recommended_quantity=None):
    source = db.query(Inventory).filter(Inventory.id == source_inventory_id).first()
    destination_warehouse = db.query(Warehouse).filter(Warehouse.id == destination_warehouse_id).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source inventory item not found.")
    if destination_warehouse is None:
        raise HTTPException(status_code=404, detail="Destination warehouse not found.")
    if source.warehouse_id == destination_warehouse.id:
        raise HTTPException(status_code=400, detail="Choose a different destination warehouse.")
    if source.quantity < quantity:
        raise HTTPException(status_code=400, detail="The source warehouse does not have enough stock.")
    expired_quantity = (
        db.query(func.sum(StockBatch.quantity))
        .filter(
            StockBatch.product_id == source.product_id,
            StockBatch.warehouse_id == source.warehouse_id,
            StockBatch.expiration_date < date.today(),
            StockBatch.quantity > 0,
        )
        .scalar()
        or 0
    )
    if source.quantity - expired_quantity < quantity:
        raise HTTPException(status_code=400, detail="This transfer would include stock from an expired batch.")
    if recommendation_inventory_id:
        recommended_item = db.query(Inventory).filter(Inventory.id == recommendation_inventory_id).first()
        if recommended_item is None or recommended_item.product_id != source.product_id or recommended_item.warehouse_id != destination_warehouse.id:
            raise HTTPException(status_code=400, detail="The recommendation does not match this product and destination.")

    destination = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == source.product_id,
            Inventory.warehouse_id == destination_warehouse.id,
        )
        .first()
    )
    details = {
        "source_inventory_id": source.id,
        "source_warehouse_id": source.warehouse_id,
        "source_quantity_before": source.quantity,
        "destination_inventory_id": destination.id if destination else None,
        "destination_warehouse_id": destination_warehouse.id,
        "destination_quantity_before": destination.quantity if destination else 0,
        "product_id": source.product_id,
        "quantity": quantity,
        "recommendation_inventory_id": recommendation_inventory_id,
        "recommended_quantity": recommended_quantity,
    }
    product = db.query(Product).filter(Product.id == source.product_id).first()
    action = StockAction(
        user_id=user_id,
        action_type="transfer",
        request_text=request_text,
        generated_sql=f"Transfer {quantity} units of {product.name} to {destination_warehouse.name}",
        details_json=json.dumps(details),
        status="pending",
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return {
        "action_id": action.id,
        "action_type": action.action_type,
        "product_name": product.name,
        "source_warehouse": db.query(Warehouse).filter(Warehouse.id == source.warehouse_id).first().name,
        "destination_warehouse": destination_warehouse.name,
        "quantity": quantity,
        "status": action.status,
    }


def confirm_stock_action(db: Session, action_id: int, user_id: int, role: str):
    action = db.query(StockAction).filter(StockAction.id == action_id).with_for_update().first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found.")
    if action.status != "pending":
        raise HTTPException(status_code=400, detail="This action is no longer pending.")
    if role != "admin" and action.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only confirm your own actions.")

    details = json.loads(action.details_json)
    if action.action_type == "set_quantity":
        inventory = db.query(Inventory).filter(Inventory.id == details["inventory_id"]).with_for_update().first()
        if inventory is None or inventory.quantity != details["quantity_before"]:
            raise HTTPException(status_code=409, detail="Stock changed after the preview. Create a new request.")
        before = inventory.quantity
        inventory.quantity = details["quantity_after"]
        decrease = max(0, before - inventory.quantity)
        batches = (
            db.query(StockBatch)
            .filter(
                StockBatch.product_id == inventory.product_id,
                StockBatch.warehouse_id == inventory.warehouse_id,
                StockBatch.quantity > 0,
            )
            .order_by(StockBatch.expiration_date.asc())
            .with_for_update()
            .all()
        )
        for batch in batches:
            used = min(batch.quantity, decrease)
            batch.quantity -= used
            decrease -= used
            if decrease == 0:
                break
        db.add(
            StockMovement(
                inventory_id=inventory.id,
                user_id=user_id,
                action_id=action.id,
                movement_type="adjustment",
                quantity_before=before,
                quantity_change=inventory.quantity - before,
                quantity_after=inventory.quantity,
                reason=action.request_text,
            )
        )
    elif action.action_type == "transfer":
        source = db.query(Inventory).filter(Inventory.id == details["source_inventory_id"]).with_for_update().first()
        if source is None or source.quantity != details["source_quantity_before"] or source.quantity < details["quantity"]:
            raise HTTPException(status_code=409, detail="Source stock changed after the preview. Create a new transfer.")
        source_before = source.quantity
        source.quantity -= details["quantity"]
        destination = None
        if details["destination_inventory_id"]:
            destination = db.query(Inventory).filter(Inventory.id == details["destination_inventory_id"]).first()
        if destination is None:
            destination = Inventory(
                product_id=details["product_id"],
                warehouse_id=details["destination_warehouse_id"],
                quantity=0,
                reorder_level=source.reorder_level,
                average_daily_demand=source.average_daily_demand,
                supplier_lead_time_days=source.supplier_lead_time_days,
            )
            db.add(destination)
            db.flush()
        else:
            destination = db.query(Inventory).filter(Inventory.id == destination.id).with_for_update().first()
        if destination.quantity != details["destination_quantity_before"]:
            raise HTTPException(status_code=409, detail="Destination stock changed after the preview. Create a new transfer.")
        destination_before = destination.quantity
        destination.quantity += details["quantity"]
        transfer_left = details["quantity"]
        source_batches = (
            db.query(StockBatch)
            .filter(
                StockBatch.product_id == source.product_id,
                StockBatch.warehouse_id == source.warehouse_id,
                StockBatch.expiration_date >= date.today(),
                StockBatch.quantity > 0,
            )
            .order_by(StockBatch.expiration_date.asc())
            .with_for_update()
            .all()
        )
        for batch in source_batches:
            moved = min(batch.quantity, transfer_left)
            if moved:
                batch.quantity -= moved
                db.add(
                    StockBatch(
                        product_id=batch.product_id,
                        warehouse_id=destination.warehouse_id,
                        lot_code=batch.lot_code,
                        quantity=moved,
                        expiration_date=batch.expiration_date,
                    )
                )
                transfer_left -= moved
            if transfer_left == 0:
                break
        db.add_all([
            StockMovement(
                inventory_id=source.id,
                user_id=user_id,
                action_id=action.id,
                movement_type="transfer_out",
                quantity_before=source_before,
                quantity_change=-details["quantity"],
                quantity_after=source.quantity,
                reason=action.request_text,
            ),
            StockMovement(
                inventory_id=destination.id,
                user_id=user_id,
                action_id=action.id,
                movement_type="transfer_in",
                quantity_before=destination_before,
                quantity_change=details["quantity"],
                quantity_after=destination.quantity,
                reason=action.request_text,
            ),
        ])
        if details.get("recommendation_inventory_id") and details.get("recommended_quantity"):
            db.add(
                RecommendationOutcome(
                    user_id=user_id,
                    inventory_id=details["recommendation_inventory_id"],
                    recommendation_type="transfer",
                    recommended_quantity=details["recommended_quantity"],
                    actual_quantity=details["quantity"],
                    accepted=True,
                    note="Transfer recommendation confirmed.",
                )
            )

    action.status = "confirmed"
    action.confirmed_at = datetime.now(timezone.utc)
    action.reviewed_at = action.confirmed_at
    action.reviewed_by_user_id = user_id
    db.commit()
    return {"action_id": action.id, "status": action.status}


def reject_stock_action(db: Session, action_id: int, user_id: int, role: str):
    action = db.query(StockAction).filter(StockAction.id == action_id).with_for_update().first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found.")
    if action.status != "pending":
        raise HTTPException(status_code=400, detail="This action is no longer pending.")
    if role != "admin" and action.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only reject your own actions.")
    action.status = "rejected"
    action.reviewed_at = datetime.now(timezone.utc)
    action.reviewed_by_user_id = user_id
    db.commit()
    return {"action_id": action.id, "status": action.status}


def get_stock_actions(db: Session, user_id: int, role: str):
    query = db.query(StockAction).order_by(StockAction.created_at.desc())
    if role != "admin":
        query = query.filter(StockAction.user_id == user_id)
    actions = query.join(User, StockAction.user_id == User.id).limit(100).all()
    return [
        {
            "id": action.id,
            "user_id": action.user_id,
            "user_email": db.query(User.email).filter(User.id == action.user_id).scalar(),
            "action_type": action.action_type,
            "request_text": action.request_text,
            "generated_sql": action.generated_sql,
            "details": json.loads(action.details_json),
            "status": action.status,
            "created_at": action.created_at,
            "confirmed_at": action.confirmed_at,
            "reviewed_at": action.reviewed_at,
            "reviewed_by_user_id": action.reviewed_by_user_id,
            "reviewed_by_email": db.query(User.email).filter(User.id == action.reviewed_by_user_id).scalar() if action.reviewed_by_user_id else None,
        }
        for action in actions
    ]


def get_stock_movements(db: Session, limit: int = 25, offset: int = 0):
    rows = (
        db.query(StockMovement, Inventory, Product, Warehouse)
        .join(Inventory, StockMovement.inventory_id == Inventory.id)
        .join(Product, Inventory.product_id == Product.id)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
        .order_by(StockMovement.created_at.desc(), StockMovement.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": movement.id,
            "product_name": product.name,
            "warehouse_name": warehouse.name,
            "movement_type": movement.movement_type,
            "quantity_before": movement.quantity_before,
            "quantity_change": movement.quantity_change,
            "quantity_after": movement.quantity_after,
            "reason": movement.reason,
            "created_at": movement.created_at,
        }
        for movement, inventory, product, warehouse in rows
    ]
