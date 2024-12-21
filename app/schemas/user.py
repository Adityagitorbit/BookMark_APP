from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    """
    Base schema for User, containing fields that are common for all user operations.
    """
    username: str = Field(..., min_length=3, max_length=50, description="The unique username of the user")
    password: str = Field(..., min_length=6, description="The password for the user (hashed later)")

    class Config:
        """
        Config class for Pydantic model
        It will help in serialization of ORM objects like SQLAlchemy.
        """
        orm_mode = True


class UserCreate(UserBase):
    """
    Schema for creating a new user, inheriting from UserBase.
    Only includes fields necessary for user creation.
    """
    pass


class UserResponse(UserBase):
    """
    Schema used for responding with user details, excluding sensitive fields.
    """
    id: int  # User's unique ID (auto-generated)

    class Config:
        orm_mode = True
