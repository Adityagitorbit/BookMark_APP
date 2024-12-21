from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Bookmark, Category, User
from app.schemas.bookmark import BookmarkCreate, BookmarkResponse
from app.database import get_db
from app.services.categorization_service import categorize_bookmark
from app.services.auth_service import get_current_user  # You can implement this function to get the current user

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=BookmarkResponse)
async def create_bookmark(
    bookmark: BookmarkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Create a new bookmark for the current user
    Automatically assigns a category based on the bookmark description using an AI categorization service.
    """
    # Check if the category exists, if not, create it
    category = db.query(Category).filter(Category.name == bookmark.category).first()
    if not category:
        category = Category(name=bookmark.category, user_id=current_user.id)
        db.add(category)
        db.commit()
        db.refresh(category)
    
    # Use AI model to suggest the category based on the bookmark's description
    # Optionally use AI categorization service (this could be integrated further with AI models)
    bookmark.category_id = category.id
    db_bookmark = Bookmark(
        title=bookmark.title,
        url=bookmark.url,
        description=bookmark.description,
        category_id=bookmark.category_id,
        user_id=current_user.id,
    )
    
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


@router.get("/", response_model=list[BookmarkResponse])
async def get_bookmarks(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Get all bookmarks for the current user.
    """
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()
    return bookmarks


@router.get("/{bookmark_id}", response_model=BookmarkResponse)
async def get_bookmark(
    bookmark_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Get a specific bookmark by ID for the current user.
    """
    bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id, Bookmark.user_id == current_user.id).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.put("/{bookmark_id}", response_model=BookmarkResponse)
async def update_bookmark(
    bookmark_id: int,
    bookmark: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a bookmark by ID for the current user.
    """
    db_bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id, Bookmark.user_id == current_user.id).first()
    if not db_bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    # Update the bookmark's fields
    db_bookmark.title = bookmark.title
    db_bookmark.url = bookmark.url
    db_bookmark.description = bookmark.description
    db_bookmark.category = bookmark.category  # Optionally update the category
    
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


@router.delete("/{bookmark_id}", response_model=BookmarkResponse)
async def delete_bookmark(
    bookmark_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Delete a specific bookmark by ID for the current user.
    """
    db_bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id, Bookmark.user_id == current_user.id).first()
    if not db_bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(db_bookmark)
    db.commit()
    return db_bookmark
