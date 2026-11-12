from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=True)
