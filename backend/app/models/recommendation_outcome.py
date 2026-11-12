from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.sql import func

from app.db.database import Base


class RecommendationOutcome(Base):
    __tablename__ = "recommendation_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    recommendation_type = Column(String(30), nullable=False)
    recommended_quantity = Column(Integer, nullable=False)
    actual_quantity = Column(Integer, nullable=True)
    accepted = Column(Boolean, nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
