from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import UserResponse, UserCreate, UserUpdate, AdminUserCreate
from crud import get_users, get_user_by_id, create_user, update_user, delete_user, get_user_by_username, get_user_by_email
from dependencies import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """List all users (admin only)"""
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Get user by ID (admin only)"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/users", response_model=UserResponse)
async def create_admin_user(
    user: AdminUserCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Create a new user (admin only)"""
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
    
    # Set admin status if specified
    if user.is_admin:
        db_user.is_admin = True
        db.commit()
        db.refresh(db_user)
    
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_admin(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Update user (admin only)"""
    db_user = update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.delete("/users/{user_id}")
async def delete_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Delete user (admin only)"""
    # Prevent admin from deleting themselves
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    if not delete_user(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}

@router.get("/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Get admin statistics"""
    total_users = len(get_users(db, skip=0, limit=10000))  # Simple count
    active_users = len([u for u in get_users(db, skip=0, limit=10000) if u.is_active])
    admin_users = len([u for u in get_users(db, skip=0, limit=10000) if u.is_admin])
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users,
        "inactive_users": total_users - active_users
    }
