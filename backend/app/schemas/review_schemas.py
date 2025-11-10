"""Review schemas for API requests and responses."""
from pydantic import BaseModel, Field
from datetime import datetime


class ReviewCreate(BaseModel):
    """Schema for creating a review."""
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1, max_length=1000)


class ReviewPublic(BaseModel):
    """Schema for public review information."""
    id: str
    product_id: str
    user_id: str
    rating: int
    comment: str
    created_at: datetime
    user_name: str = ""  # Populated from user data
    
    class Config:
        from_attributes = True
