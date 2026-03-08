from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from app.models import UserRole

class CategoryBase(BaseModel):
    name: str

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal = Field(gt=0) 
    stock: int = Field(ge=0)     
    category_id: int

class UserCreate(BaseModel):
    name: str 
    email: EmailStr
    password: str
    role: UserRole = UserRole.customer

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True 

class ProductCreate(ProductBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int
    
class CartItemResponse(BaseModel):
    id: int
    quantity: int
    product_id: int
    item_details: ProductResponse 

    class Config:
        from_attributes = True

class OrderItemResponse(BaseModel):
    id: int
    price_at_purchase: Decimal
    quantity: int
    product_id: int

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total_price: Decimal
    status: str
    created_at: datetime
    user_id: int
    client_secret: Optional[str] = None

    class Config:
        from_attributes = True
        
class TokenData(BaseModel):
    id: Optional[int] = None