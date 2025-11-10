"""Review model for product reviews and ratings."""
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field
from beanie import PydanticObjectId


class Review(Document):
    """Review document model."""
    
    product_id: Indexed(PydanticObjectId)  # type: ignore
    user_id: Indexed(PydanticObjectId)  # type: ignore
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "reviews"
        indexes = [
            "product_id",
            "user_id"
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "507f1f77bcf86cd799439011",
                "user_id": "507f191e810c19729de860ea",
                "rating": 5,
                "comment": "Excellent product! Highly recommended."
            }
        }
