import re
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.constants import ORDER_STATUSES
from app.schemas.product import Product

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{9,14}$")

class OrderItemBase(BaseModel):
    product_id: UUID
    quantity: int = Field(..., ge=1)
    size: str = Field(..., min_length=1)
    unit_price: Decimal = Field(..., ge=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: UUID
    order_id: UUID
    product: Optional[Product] = None

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    session_id: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    address: str = Field(..., min_length=1, max_length=500)
    total_amount: Decimal = Field(..., ge=0)
    status: str = Field("demo")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-]", "", v)
        if not PHONE_REGEX.match(cleaned):
            raise ValueError("Invalid phone number format. Should be international format like +91XXXXXXXXXX")
        return cleaned

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ORDER_STATUSES:
            raise ValueError(f"Invalid order status. Must be one of {ORDER_STATUSES}")
        return v

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: UUID
    created_at: datetime
    items: List[OrderItem] = []

    model_config = ConfigDict(from_attributes=True)

class CheckoutRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    address: str = Field(..., min_length=1, max_length=500)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-]", "", v)
        if not PHONE_REGEX.match(cleaned):
            raise ValueError("Invalid phone number format. Should be international format like +91XXXXXXXXXX")
        return cleaned

class CheckoutResponse(BaseModel):
    success: bool
    message: str
    order_id: Optional[UUID] = None
