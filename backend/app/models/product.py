"""Product model for product catalog."""
from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field
from pymongo import IndexModel, TEXT


class Product(Document):
    """Product document model."""
    
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    imageUrl: str
    category: Indexed(str)  # type: ignore
    stock_quantity: int = Field(..., ge=0)
    avg_rating: float = Field(default=0.0, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "products"
        indexes = [
            IndexModel([("name", TEXT), ("description", TEXT)]),
            "category"
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse with USB receiver",
                "price": 29.99,
                "imageUrl": "https://example.com/images/mouse.jpg",
                "category": "Electronics",
                "stock_quantity": 100
            }
        }
