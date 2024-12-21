from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Bookmark(Base):
    """
    Bookmark model for database table `bookmarks`
    Each bookmark belongs to a user and a category.
    """
    __tablename__ = "bookmarks"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each bookmark
    title = Column(String, index=True)  # Title of the bookmark
    url = Column(String, unique=True, index=True)  # URL of the bookmark
    description = Column(Text)  # Optional: A description of the bookmark

    # Foreign key linking the bookmark to a category
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Foreign key linking the bookmark to a user
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to the User model (One user can have many bookmarks)
    user = relationship("User", back_populates="bookmarks")

    # Relationship to the Category model (One category can have many bookmarks)
    category = relationship("Category", back_populates="bookmarks")
