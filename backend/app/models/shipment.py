from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from app.db.database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
    )

    status = Column(String)

    destination = Column(String)