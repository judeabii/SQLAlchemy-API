from pydantic import BaseModel, EmailStr
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


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
