from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Enum
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    admin = "admin"
    customer = "customer"
    seller = "seller"

class User(Base):
    __tablename__="users"
    
    id= Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.customer)
    
    orders = relationship("Order", back_populates="user", lazy="selectin")
    cart_items = relationship("CartItem", back_populates="owner", lazy="selectin")
    
    
class Category(Base):
    __tablename__="categories"
    
    id= Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    products = relationship("Product", back_populates="category")
    
class Product(Base):
    __tablename__="products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    price = Column(Numeric, nullable=False)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    
    cart_entries = relationship("CartItem", back_populates="item_details")
    category = relationship("Category", back_populates="products")
    
class CartItem(Base):
    __tablename__="cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    item_details = relationship("Product", back_populates="cart_entries", lazy="selectin")
    owner = relationship("User", back_populates="cart_items")
    
class Order(Base):
    __tablename__="orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Numeric, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", lazy="selectin")
    
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    price_at_purchase = Column(Numeric, nullable=False) 
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")