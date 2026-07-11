from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(String)

    city = Column(String)

    manager = Column(String)