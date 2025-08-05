from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from schemas import UserLogin, Token, UserCreate, UserResponse, PasswordChange
from crud import authenticate_user, create_user, get_user_by_username, get_user_by_email, update_last_login, blacklist_token, change_password
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password
from dependencies import get_current_user, get_token_from_request

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if username already exists
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    db_user = create_user(db, user)
    return db_user

@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Update last login
    update_last_login(db, user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/logout")
async def logout(
    token: str = Depends(get_token_from_request),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Logout user by blacklisting the token"""
    blacklist_token(db, token)
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/change-password")
async def change_user_password(
    password_change: PasswordChange,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    # Verify current password
    if not verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Change password
    if change_password(db, current_user, password_change.new_password):
        return {"message": "Password changed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )

@router.get("/verify-token")
async def verify_token_endpoint(current_user = Depends(get_current_user)):
    """Verify if token is valid"""
    return {
        "valid": True,
        "user_id": current_user.id,
        "username": current_user.username,
        "is_admin": current_user.is_admin
    }
