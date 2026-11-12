from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.product import Product
from app.models.stock_batch import StockBatch
from app.models.stock_movement import StockMovement
from app.models.warehouse import Warehouse


def add_stock_batch(db: Session, batch, user_id: int):
    if batch.expiration_date < date.today():
        raise HTTPException(status_code=400, detail="Expiration date must be today or later.")

    product = db.query(Product).filter(Product.id == batch.product_id).first()
    warehouse = db.query(Warehouse).filter(Warehouse.id == batch.warehouse_id).first()
    if product is None or warehouse is None:
        raise HTTPException(status_code=404, detail="Product or warehouse not found.")

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == batch.product_id,
            Inventory.warehouse_id == batch.warehouse_id,
        )
        .first()
    )
    if inventory is None:
        inventory = Inventory(
            product_id=batch.product_id,
            warehouse_id=batch.warehouse_id,
            quantity=0,
            reorder_level=0,
            average_daily_demand=0,
            supplier_lead_time_days=0,
        )
        db.add(inventory)
        db.flush()

    before = inventory.quantity
    inventory.quantity += batch.quantity
    stock_batch = StockBatch(
        product_id=batch.product_id,
        warehouse_id=batch.warehouse_id,
        lot_code=batch.lot_code,
        quantity=batch.quantity,
        expiration_date=batch.expiration_date,
    )
    db.add(stock_batch)
    db.flush()
    db.add(
        StockMovement(
            inventory_id=inventory.id,
            user_id=user_id,
            movement_type="batch_received",
            quantity_before=before,
            quantity_change=batch.quantity,
            quantity_after=inventory.quantity,
            reason=f"Received lot {batch.lot_code}",
        )
    )
    db.commit()
    return {"id": stock_batch.id, "quantity": stock_batch.quantity, "lot_code": stock_batch.lot_code}


def get_expiring_batches(db: Session, days: int = 30):
    cutoff = date.today() + timedelta(days=max(0, min(days, 365)))
    rows = (
        db.query(StockBatch, Product, Warehouse)
        .join(Product, StockBatch.product_id == Product.id)
        .join(Warehouse, StockBatch.warehouse_id == Warehouse.id)
        .filter(StockBatch.expiration_date <= cutoff, StockBatch.quantity > 0)
        .order_by(StockBatch.expiration_date.asc())
        .all()
    )
    return [
        {
            "id": batch.id,
            "product_id": product.id,
            "product_name": product.name,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "lot_code": batch.lot_code,
            "quantity": batch.quantity,
            "expiration_date": batch.expiration_date,
            "days_until_expiration": (batch.expiration_date - date.today()).days,
        }
        for batch, product, warehouse in rows
    ]


def write_off_expired_batch(db: Session, batch_id: int, user_id: int):
    batch = db.query(StockBatch).filter(StockBatch.id == batch_id).with_for_update().first()
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found.")
    if batch.expiration_date >= date.today():
        raise HTTPException(status_code=400, detail="Only expired batches can be written off.")
    if batch.quantity == 0:
        raise HTTPException(status_code=400, detail="This batch has already been written off.")

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == batch.product_id,
            Inventory.warehouse_id == batch.warehouse_id,
        )
        .with_for_update()
        .first()
    )
    if inventory is None or inventory.quantity < batch.quantity:
        raise HTTPException(status_code=409, detail="Inventory quantity does not match this batch.")

    before = inventory.quantity
    written_off = batch.quantity
    inventory.quantity -= written_off
    batch.quantity = 0
    db.add(
        StockMovement(
            inventory_id=inventory.id,
            user_id=user_id,
            movement_type="expiry_writeoff",
            quantity_before=before,
            quantity_change=-written_off,
            quantity_after=inventory.quantity,
            reason=f"Expired lot {batch.lot_code} written off",
        )
    )
    db.commit()
    return {"batch_id": batch.id, "written_off": written_off, "quantity_after": inventory.quantity}
