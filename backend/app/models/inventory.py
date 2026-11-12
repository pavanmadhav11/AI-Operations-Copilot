from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Float,
    Index,
)

from app.db.database import Base


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (Index("ix_inventory_product_warehouse", "product_id", "warehouse_id"),)

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
    )

    quantity = Column(Integer)

    reorder_level = Column(Integer)

    average_daily_demand = Column(Float, nullable=False, default=0)

    supplier_lead_time_days = Column(Integer, nullable=False, default=0)
