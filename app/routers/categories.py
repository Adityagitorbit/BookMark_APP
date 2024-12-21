from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import Category, User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.database import get_db
from app.services.categorization_service import categorize_link  # AI-based categorization service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Create a new category for the current user.
    """
    # Check if category name already exists
    existing_category = db.query(Category).filter(Category.name == category.name, Category.user_id == current_user.id).first()
    if existing_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists.")

    # Create and add the new category
    db_category = Category(name=category.name, user_id=current_user.id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve all categories for the current user.
    """
    categories = db.query(Category).filter(Category.user_id == current_user.id).all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_by_id(
    category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific category by its ID for the current user.
    """
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a category for the current user.
    """
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    db_category.name = category.name  # Update category name
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(
    category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Delete a category by its ID for the current user.
    """
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return db_category


@router.post("/categorize-link/", response_model=CategoryResponse)
def categorize_bookmark_link(
    url: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    AI-based categorization of a link (bookmark URL).
    """
    # AI categorization logic
    category_name = categorize_link(url)
    
    # Create and add the new category if it doesn't exist already
    existing_category = db.query(Category).filter(Category.name == category_name, Category.user_id == current_user.id).first()
    if not existing_category:
        db_category = Category(name=category_name, user_id=current_user.id)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    return existing_category
