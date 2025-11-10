"""User schemas for API requests and responses."""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """Schema for public user information."""
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool
    
    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """Schema for JWT token data."""
    user_id: Optional[str] = None
    email: Optional[str] = None


class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
