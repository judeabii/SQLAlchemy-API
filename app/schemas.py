from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    price: int
    is_sale: Optional[bool] = False


class CreateProduct(ProductBase):
    is_sale: bool


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
