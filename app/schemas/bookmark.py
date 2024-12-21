from pydantic import BaseModel
from typing import Optional

class BookmarkBase(BaseModel):
    """
    Base schema for the Bookmark, used for both creation and update.
    """
    title: str  # Title of the bookmark
    url: str  # URL of the bookmark
    description: Optional[str] = None  # Description is optional

class BookmarkCreate(BookmarkBase):
    """
    Schema for creating a new bookmark. Inherits from BookmarkBase.
    """
    pass

class BookmarkUpdate(BookmarkBase):
    """
    Schema for updating an existing bookmark. Inherits from BookmarkBase.
    """
    pass

class BookmarkInResponse(BookmarkBase):
    """
    Schema for the response after a bookmark is created or fetched.
    Includes the ID and category of the bookmark.
    """
    id: int  # ID of the bookmark
    category_id: int  # ID of the associated category

    class Config:
        orm_mode = True  # Allows the model to be used with ORM objects like SQLAlchemy models

class BookmarkOut(BookmarkBase):
    """
    Schema for the response when fetching a bookmark.
    Does not include sensitive fields like `user_id`.
    """
    id: int  # ID of the bookmark
    user_id: int  # ID of the associated user
    category_id: int  # ID of the associated category

    class Config:
        orm_mode = True  # Allows the model to be used with ORM objects like SQLAlchemy models
