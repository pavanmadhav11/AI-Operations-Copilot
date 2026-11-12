from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.db.database import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_file_id = Column(Integer, ForeignKey("uploaded_files.id"), nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=True)
    quote_reference = Column(String(100), nullable=True)
    items_json = Column(Text, nullable=False)
    total_amount = Column(Float, nullable=False, default=0)
    recommended_quantity = Column(Integer, nullable=True)
    status = Column(String(20), nullable=False, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
