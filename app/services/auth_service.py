from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.utils import verify_token  # You can implement this function to verify JWT tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    This function extracts the current user from the token and validates it.
    The `token` is passed via the `Authorization` header in the form of Bearer Token.
    """
    user_id = verify_token(token)  # Decode the token and extract user info
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
