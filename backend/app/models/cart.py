"""Cart model for shopping cart management."""
from datetime import datetime
from typing import List
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class CartItem(BaseModel):
    """Cart item embedded model."""
    product_id: PydanticObjectId
    quantity: int = Field(..., gt=0)


class Cart(Document):
    """Cart document model."""
    
    user_id: Indexed(PydanticObjectId, unique=True)  # type: ignore
    items: List[CartItem] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "carts"
        indexes = [
            "user_id"
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "507f191e810c19729de860ea",
                "items": [
                    {
                        "product_id": "507f1f77bcf86cd799439011",
                        "quantity": 2
                    }
                ]
            }
        }
