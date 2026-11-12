from pydantic import BaseModel, Field


class PurchaseOrderItem(BaseModel):
    product_name: str = Field(min_length=1, max_length=150)
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)
    source_page: int | None = Field(default=None, gt=0)


class PurchaseOrderDraftRequest(BaseModel):
    supplier_name: str = Field(min_length=1, max_length=200)
    supplier_email: str | None = None
    quote_reference: str | None = None
    lead_time_days: int | None = Field(default=None, ge=0)
    items: list[PurchaseOrderItem] = Field(min_length=1)
    inventory_id: int | None = Field(default=None, gt=0)
    recommended_quantity: int | None = Field(default=None, gt=0)
