from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.stock_movement import StockMovement


def get_inventory(db: Session, limit: int | None = None, offset: int = 0):
    query = (
        db.query(Inventory, Product, Warehouse)
        .join(Product, Inventory.product_id == Product.id)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
        .order_by(Product.name.asc(), Inventory.id.asc())
    )
    if limit is not None:
        query = query.offset(offset).limit(limit)
    rows = query.all()

    return [
        {
            "id": inventory.id,
            "product_id": product.id,
            "product_name": product.name,
            "category": product.category,
            "price": product.price,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "quantity": inventory.quantity,
            "reorder_level": inventory.reorder_level,
            "average_daily_demand": inventory.average_daily_demand,
            "supplier_lead_time_days": inventory.supplier_lead_time_days,
            "days_until_stockout": round(inventory.quantity / inventory.average_daily_demand, 1) if inventory.average_daily_demand else None,
        }
        for inventory, product, warehouse in rows
    ]


def get_warehouses(db: Session):
    return db.query(Warehouse).order_by(Warehouse.name.asc()).all()


def add_warehouse(db: Session, warehouse_data):
    warehouse = Warehouse(
        name=warehouse_data.name,
        city=warehouse_data.city,
        manager=warehouse_data.manager,
    )
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


def add_inventory_item(db: Session, item, user_id: int):
    warehouse = db.query(Warehouse).filter(Warehouse.id == item.warehouse_id).first()
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found.")

    product = Product(name=item.name, category=item.category, price=item.price)
    db.add(product)
    db.flush()

    inventory = Inventory(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity=item.quantity,
        reorder_level=item.reorder_level,
        average_daily_demand=item.average_daily_demand,
        supplier_lead_time_days=item.supplier_lead_time_days,
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    db.add(
        StockMovement(
            inventory_id=inventory.id,
            user_id=user_id,
            movement_type="opening_stock",
            quantity_before=0,
            quantity_change=item.quantity,
            quantity_after=item.quantity,
            reason="Initial inventory item setup",
        )
    )
    db.commit()

    return {
        "id": inventory.id,
        "product_id": product.id,
        "product_name": product.name,
        "category": product.category,
        "price": product.price,
        "warehouse_id": warehouse.id,
        "warehouse_name": warehouse.name,
        "quantity": inventory.quantity,
        "reorder_level": inventory.reorder_level,
        "average_daily_demand": inventory.average_daily_demand,
        "supplier_lead_time_days": inventory.supplier_lead_time_days,
        "days_until_stockout": round(inventory.quantity / inventory.average_daily_demand, 1) if inventory.average_daily_demand else None,
    }
