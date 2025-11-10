"""Product schemas for API requests and responses."""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ProductCreate(BaseModel):
    """Schema for creating a product."""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    imageUrl: str
    category: str = Field(..., min_length=1)
    stock_quantity: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    imageUrl: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1)
    stock_quantity: Optional[int] = Field(None, ge=0)


class ProductPublic(BaseModel):
    """Schema for public product information."""
    id: str
    name: str
    description: str
    price: float
    imageUrl: str
    category: str
    stock_quantity: int
    avg_rating: float
    review_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
