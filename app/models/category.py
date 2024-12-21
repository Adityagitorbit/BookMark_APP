from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    """
    Category model for database table `categories`
    Each category can contain multiple bookmarks.
    """
    __tablename__ = "categories"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each category
    name = Column(String, unique=True, index=True)  # Name of the category

    # Foreign key linking the category to a user
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to the User model (One user can have many categories)
    user = relationship("User", back_populates="categories")

    # Relationship to the Bookmark model (One category can have many bookmarks)
    bookmarks = relationship("Bookmark", back_populates="category")
