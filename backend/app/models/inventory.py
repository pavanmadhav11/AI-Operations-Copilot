from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)

from app.db.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

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