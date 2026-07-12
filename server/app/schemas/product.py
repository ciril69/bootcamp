from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ProductImageBase(BaseModel):
    image_url: str = Field(..., min_length=1)
    display_order: int = Field(0, ge=0)

class ProductImageCreate(ProductImageBase):
    product_id: UUID

class ProductImage(ProductImageBase):
    id: UUID
    product_id: UUID

    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    category_id: UUID
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    price: Decimal = Field(..., ge=0)
    stock: int = Field(0, ge=0)
    featured: bool = Field(False)
    customization_available: bool = Field(True)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: UUID
    created_at: datetime
    images: List[ProductImage] = []

    model_config = ConfigDict(from_attributes=True)
