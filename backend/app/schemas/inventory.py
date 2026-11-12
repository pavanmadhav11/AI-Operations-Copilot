from datetime import date
from pydantic import BaseModel, Field


class InventoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    category: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    reorder_level: int = Field(ge=0)
    warehouse_id: int = Field(gt=0)
    average_daily_demand: float = Field(default=0, ge=0)
    supplier_lead_time_days: int = Field(default=0, ge=0)


class StockBatchCreate(BaseModel):
    product_id: int = Field(gt=0)
    warehouse_id: int = Field(gt=0)
    lot_code: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    expiration_date: date


class TransferPreviewRequest(BaseModel):
    source_inventory_id: int = Field(gt=0)
    destination_warehouse_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    recommendation_inventory_id: int | None = Field(default=None, gt=0)
    recommended_quantity: int | None = Field(default=None, gt=0)


class WarehouseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    city: str = Field(min_length=1, max_length=100)
    manager: str = Field(default="", max_length=100)


class RecommendationFeedback(BaseModel):
    inventory_id: int = Field(gt=0)
    recommendation_type: str
    recommended_quantity: int = Field(gt=0)
    accepted: bool
    note: str | None = None


class InventoryItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    category: str
    price: float
    warehouse_id: int
    warehouse_name: str
    quantity: int
    reorder_level: int


class WarehouseResponse(BaseModel):
    id: int
    name: str
    city: str | None
