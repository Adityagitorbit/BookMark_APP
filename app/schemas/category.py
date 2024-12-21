from pydantic import BaseModel
from typing import List, Optional

class CategoryBase(BaseModel):
    """
    Base schema that defines the common fields for creating and updating a category
    """
    name: str  # Name of the category

    class Config:
        orm_mode = True  # Tells Pydantic to treat the ORM model as a dict


class CategoryCreate(CategoryBase):
    """
    Schema for creating a category
    Inherits from CategoryBase and adds no extra fields
    """
    pass


class CategoryUpdate(CategoryBase):
    """
    Schema for updating a category
    Inherits from CategoryBase and adds no extra fields
    """
    pass


class Category(CategoryBase):
    """
    Schema used to return category data from the database
    """
    id: int  # ID of the category

    class Config:
        orm_mode = True  # Tells Pydantic to treat the ORM model as a dict
