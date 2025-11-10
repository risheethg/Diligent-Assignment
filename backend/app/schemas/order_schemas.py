"""Order schemas for API requests and responses."""
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class ShippingAddressSchema(BaseModel):
    """Schema for shipping address."""
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., min_length=5, max_length=10)


class OrderItemSchema(BaseModel):
    """Schema for order item."""
    product_id: str
    name: str
    price: float
    quantity: int


class OrderCreate(BaseModel):
    """Schema for creating an order."""
    payment_intent_id: str
    shipping_address: ShippingAddressSchema


class OrderPublic(BaseModel):
    """Schema for public order information."""
    id: str
    user_id: str
    items: List[OrderItemSchema]
    total_amount: float
    shipping_address: ShippingAddressSchema
    status: str
    stripe_payment_intent_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaymentIntentResponse(BaseModel):
    """Schema for payment intent response."""
    clientSecret: str
    amount: float
