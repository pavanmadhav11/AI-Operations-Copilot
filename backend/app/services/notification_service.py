from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.purchase_order import PurchaseOrder
from app.models.stock_action import StockAction
from app.models.stock_batch import StockBatch
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.services.dashboard_service import get_low_stock_inventory


def get_notifications(db: Session, user_id: int, role: str):
    events = []
    for alert in get_low_stock_inventory(db):
        events.append({
            "source_key": f"low_stock:{alert['id']}",
            "title": f"Low stock: {alert['product_name']}",
            "message": f"{alert['quantity']} left at {alert['warehouse_name']}; reorder level is {alert['reorder_level']}.",
            "link": "/inventory",
        })

    cutoff = date.today() + timedelta(days=30)
    batch_rows = (
        db.query(StockBatch, Product, Warehouse)
        .join(Product, StockBatch.product_id == Product.id)
        .join(Warehouse, StockBatch.warehouse_id == Warehouse.id)
        .filter(StockBatch.expiration_date <= cutoff, StockBatch.quantity > 0)
        .all()
    )
    for batch, product, warehouse in batch_rows:
        events.append({
            "source_key": f"expiry:{batch.id}",
            "title": f"Expiry alert: {product.name}",
            "message": f"Lot {batch.lot_code} has {batch.quantity} units at {warehouse.name} and expires {batch.expiration_date}.",
            "link": "/inventory/batches",
        })

    actions_query = db.query(StockAction).filter(StockAction.status == "pending")
    orders_query = db.query(PurchaseOrder).filter(PurchaseOrder.status == "draft")
    if role != "admin":
        actions_query = actions_query.filter(StockAction.user_id == user_id)
        orders_query = orders_query.filter(PurchaseOrder.user_id == user_id)
    for action in actions_query.all():
        events.append({
            "source_key": f"action:{action.id}",
            "title": "Stock change needs review",
            "message": action.request_text,
            "link": "/inventory/actions",
        })
    for order in orders_query.all():
        events.append({
            "source_key": f"purchase_order:{order.id}",
            "title": f"Purchase order draft #{order.id}",
            "message": "Review the draft before sending it to the supplier.",
            "link": "/procurement",
        })

    current_keys = {event["source_key"] for event in events}
    saved = {
        notification.source_key: notification
        for notification in db.query(Notification).filter(Notification.user_id == user_id).all()
    }
    for event in events:
        notification = saved.get(event["source_key"])
        if notification is None:
            db.add(Notification(user_id=user_id, **event))
        else:
            if not notification.is_active:
                notification.is_read = False
            notification.title = event["title"]
            notification.message = event["message"]
            notification.link = event["link"]
            notification.is_active = True
    for key, notification in saved.items():
        if key not in current_keys:
            notification.is_active = False
    db.commit()
    return [
        {
            "id": item.id,
            "title": item.title,
            "message": item.message,
            "link": item.link,
            "is_read": item.is_read,
            "created_at": item.created_at,
        }
        for item in db.query(Notification)
        .filter(Notification.user_id == user_id, Notification.is_active.is_(True))
        .order_by(Notification.is_read.asc(), Notification.created_at.desc())
        .limit(25)
        .all()
    ]


def mark_notification_read(db: Session, notification_id: int, user_id: int):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id,
    ).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found.")
    notification.is_read = True
    db.commit()
    return {"id": notification.id, "is_read": notification.is_read}
