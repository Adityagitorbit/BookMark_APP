from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    """
    User model for database table `users`
    Stores user information like `username` and `hashed_password`
    """
    __tablename__ = "users"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each user
    username = Column(String, unique=True, index=True)  # Unique username for login
    hashed_password = Column(String)  # Hashed password for security

    # Optional: Define a relationship if you want to link users with bookmarks or categories
    # bookmarks = relationship("Bookmark", back_populates="owner")  # If bookmarks are linked to the user
