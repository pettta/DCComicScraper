from sqlalchemy.orm import Session
from database import User, TokenBlacklist
from auth import get_password_hash, verify_password
from schemas import UserCreate, UserUpdate
from datetime import datetime
from typing import Optional, List

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get list of users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user information"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def update_last_login(db: Session, user: User):
    """Update user's last login timestamp"""
    user.last_login = datetime.utcnow()
    db.commit()

def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def blacklist_token(db: Session, token: str):
    """Add token to blacklist"""
    blacklisted_token = TokenBlacklist(token=token)
    db.add(blacklisted_token)
    db.commit()

def is_token_blacklisted(db: Session, token: str) -> bool:
    """Check if token is blacklisted"""
    return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None

def change_password(db: Session, user: User, new_password: str) -> bool:
    """Change user password"""
    try:
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        return True
    except Exception:
        return False
