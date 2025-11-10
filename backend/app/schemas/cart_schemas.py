"""Cart schemas for API requests and responses."""
from typing import List, Optional
from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    """Schema for adding an item to cart."""
    product_id: str
    quantity: int = Field(..., gt=0)


class CartItemUpdate(BaseModel):
    """Schema for updating cart item quantity."""
    quantity: int = Field(..., gt=0)


class ProductInCart(BaseModel):
    """Schema for product details in cart."""
    id: str
    name: str
    price: float
    imageUrl: str
    stock_quantity: int


class CartItemPublic(BaseModel):
    """Schema for cart item with populated product details."""
    product_id: str
    quantity: int
    product: Optional[ProductInCart] = None


class CartPublic(BaseModel):
    """Schema for public cart information."""
    id: str
    user_id: str
    items: List[CartItemPublic]
    total: float = 0.0
    
    class Config:
        from_attributes = True
