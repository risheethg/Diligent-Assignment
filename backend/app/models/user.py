"""User model for authentication and user management."""
from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    """User document model."""
    
    email: Indexed(EmailStr, unique=True)  # type: ignore
    hashed_password: str
    first_name: str
    last_name: str
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_admin": False
            }
        }
