from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.database import get_db
from app.services.auth_service import hash_password, verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Takes user input data (username and password), hashes the password, and stores the user in the database.
    """
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password before saving
    hashed_password = hash_password(user.password)

    # Create new user
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=UserResponse)
async def login_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Log in a user. Verifies if the password matches and returns the user information if valid.
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return db_user


@router.get("/me", response_model=UserResponse)
async def get_current_user(db: Session = Depends(get_db)):
    """
    Get the current user's details.
    This assumes that the user is already authenticated (you will need authentication for this route).
    """
    # For now, we just return a placeholder, as we don't have authentication in place yet
    db_user = db.query(User).first()  # Replace with actual user identification logic
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
