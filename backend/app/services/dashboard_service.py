from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.chat import ChatMessage
from app.models.chat_session import ChatSession
from app.models.uploaded_file import UploadedFile
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.warehouse import Warehouse


def get_dashboard_stats(db: Session, user_id: int, role: str):
    document_query = db.query(UploadedFile)
    message_query = db.query(ChatMessage).join(ChatSession)
    if role != "admin":
        document_query = document_query.filter(UploadedFile.user_id == user_id)
        message_query = message_query.filter(ChatSession.user_id == user_id)

    users = (db.query(func.count(User.id)).scalar() or 0) if role == "admin" else 1
    documents = document_query.with_entities(func.count(UploadedFile.id)).scalar() or 0
    ai_requests = message_query.filter(ChatMessage.role == "user").with_entities(func.count(ChatMessage.id)).scalar() or 0
    total_storage = document_query.with_entities(
        func.sum(func.length(UploadedFile.extracted_text))
    ).scalar() or 0

    storage = round(total_storage / (1024 * 1024), 2)

    return {
        "users": users,
        "documents": documents,
        "aiRequests": ai_requests,
        "storage": f"{storage} MB",
    }


def get_low_stock_inventory(db: Session):
    rows = (
        db.query(Inventory, Product, Warehouse)
        .join(Product, Inventory.product_id == Product.id)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
        .filter(Inventory.quantity < Inventory.reorder_level)
        .order_by(Inventory.quantity.asc())
        .all()
    )

    product_ids = {inventory.product_id for inventory, _, _ in rows}
    sources_by_product = {}
    if product_ids:
        source_rows = (
            db.query(Inventory, Warehouse)
            .join(Warehouse, Inventory.warehouse_id == Warehouse.id)
            .filter(
                Inventory.product_id.in_(product_ids),
                Inventory.quantity > Inventory.reorder_level,
            )
            .all()
        )
        for source, source_warehouse in source_rows:
            sources_by_product.setdefault(source.product_id, []).append(
                {
                    "warehouse_name": source_warehouse.name,
                    "inventory_id": source.id,
                    "surplus": source.quantity - source.reorder_level,
                }
            )

    alerts = []
    for inventory, product, warehouse in rows:
        days_left = (
            round(inventory.quantity / inventory.average_daily_demand, 1)
            if inventory.average_daily_demand
            else None
        )
        needed = max(1, (inventory.reorder_level * 2) - inventory.quantity)
        sources = [
            source
            for source in sources_by_product.get(inventory.product_id, [])
            if source["inventory_id"] != inventory.id
        ]
        sources.sort(key=lambda source: source["surplus"], reverse=True)
        available_transfer = sources[0]["surplus"] if sources else 0
        transfer_quantity = min(needed, available_transfer)
        order_quantity = max(0, needed - transfer_quantity)
        if transfer_quantity and order_quantity:
            recommendation = "Transfer available stock, then reorder the remaining amount."
        elif transfer_quantity:
            recommendation = "Transfer stock from another warehouse before placing a new order."
        else:
            recommendation = "Prepare a supplier reorder. No other warehouse has surplus stock."

        alerts.append(
            {
                "id": inventory.id,
                "product_id": product.id,
                "product_name": product.name,
                "warehouse_id": warehouse.id,
                "warehouse_name": warehouse.name,
                "quantity": inventory.quantity,
                "reorder_level": inventory.reorder_level,
                "average_daily_demand": inventory.average_daily_demand,
                "supplier_lead_time_days": inventory.supplier_lead_time_days,
                "days_until_stockout": days_left,
                "risk_reason": (
                    f"About {days_left} days of stock remain; supplier lead time is {inventory.supplier_lead_time_days} days."
                    if days_left is not None
                    else f"Stock is below the reorder level. Add average daily demand to estimate stockout timing."
                ),
                "recommended_action": recommendation,
                "recommended_transfer_quantity": transfer_quantity,
                "recommended_order_quantity": order_quantity,
                "suggested_transfer_source": sources[0] if sources else None,
            }
        )

    alerts.sort(
        key=lambda item: (
            item["days_until_stockout"] is None,
            item["days_until_stockout"] if item["days_until_stockout"] is not None else float("inf"),
        )
    )
    return alerts


def get_recent_documents(db: Session, user_id: int, role: str):
    query = db.query(UploadedFile)
    if role != "admin":
        query = query.filter(UploadedFile.user_id == user_id)
    docs = query.order_by(UploadedFile.uploaded_at.desc()).limit(5).all()

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
        }
        for doc in docs
    ]


def get_recent_activity(db: Session, user_id: int, role: str):
    query = db.query(ChatMessage).join(ChatSession)
    if role != "admin":
        query = query.filter(ChatSession.user_id == user_id)
    chats = query.order_by(ChatMessage.created_at.desc()).limit(5).all()

    return [
        {
            "text": f"{msg.role.title()} message"
        }
        for msg in chats
    ]


def get_activity_chart(db: Session, user_id: int, role: str):
    query = db.query(
            func.date(ChatMessage.created_at),
            func.count(ChatMessage.id),
        ).join(ChatSession)
    if role != "admin":
        query = query.filter(ChatSession.user_id == user_id)
    data = query.group_by(func.date(ChatMessage.created_at)).order_by(func.date(ChatMessage.created_at)).all()

    return [
        {
            "date": str(day),
            "requests": count,
        }
        for day, count in data
    ]
