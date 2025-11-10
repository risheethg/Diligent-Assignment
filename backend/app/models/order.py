"""Order model for order management."""
from datetime import datetime
from typing import List
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class OrderItem(BaseModel):
    """Order item embedded model."""
    product_id: PydanticObjectId
    name: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class ShippingAddress(BaseModel):
    """Shipping address embedded model."""
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., min_length=5, max_length=10)


class Order(Document):
    """Order document model."""
    
    user_id: Indexed(PydanticObjectId)  # type: ignore
    items: List[OrderItem]
    total_amount: float = Field(..., gt=0)
    shipping_address: ShippingAddress
    status: str = Field(default="pending")  # pending, processing, shipped, delivered, cancelled
    stripe_payment_intent_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "orders"
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
                        "name": "Wireless Mouse",
                        "price": 29.99,
                        "quantity": 2
                    }
                ],
                "total_amount": 59.98,
                "shipping_address": {
                    "street": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip_code": "10001"
                },
                "status": "pending",
                "stripe_payment_intent_id": "pi_1234567890"
            }
        }
