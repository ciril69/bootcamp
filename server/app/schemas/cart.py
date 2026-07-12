from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.constants import AVAILABLE_SIZES
from app.schemas.product import Product

class CartItemBase(BaseModel):
    session_id: str = Field(..., min_length=1)
    product_id: UUID
    size: str = Field(..., min_length=1)
    quantity: int = Field(1, ge=1)

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: str) -> str:
        v_upper = v.upper()
        if v_upper not in AVAILABLE_SIZES:
            raise ValueError(f"Invalid size. Must be one of {AVAILABLE_SIZES}")
        return v_upper

class CartItemCreate(BaseModel):
    session_id: str = Field(..., min_length=1)
    product_id: UUID
    size: str = Field(..., min_length=1)
    quantity: int = Field(1, ge=1)

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: str) -> str:
        v_upper = v.upper()
        if v_upper not in AVAILABLE_SIZES:
            raise ValueError(f"Invalid size. Must be one of {AVAILABLE_SIZES}")
        return v_upper

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

class CartItem(CartItemBase):
    id: UUID
    created_at: datetime
    product: Optional[Product] = None

    model_config = ConfigDict(from_attributes=True)

class Cart(BaseModel):
    session_id: str
    items: List[CartItem] = []
    subtotal: Decimal = Field(Decimal("0.00"), ge=0)

    model_config = ConfigDict(from_attributes=True)
