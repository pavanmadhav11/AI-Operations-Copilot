from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.sql import func

from app.db.database import Base


class SalesRecord(Base):
    __tablename__ = "sales_records"
    __table_args__ = (
        UniqueConstraint("source_file_id", "product_id", "sale_date"),
        Index("ix_sales_records_date_product", "sale_date", "product_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    source_file_id = Column(Integer, ForeignKey("uploaded_files.id"), nullable=False)
    sale_date = Column(Date, nullable=False)
    units_sold = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
