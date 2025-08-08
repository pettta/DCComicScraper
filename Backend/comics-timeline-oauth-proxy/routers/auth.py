from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from schemas import UserLogin, Token, UserCreate, UserResponse, PasswordChange, EmailVerificationResponse
from crud import authenticate_user, create_user, get_user_by_username, get_user_by_email, update_last_login, blacklist_token, change_password, verify_user_email
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password
from dependencies import get_current_user, get_token_from_request
from email_service import create_verification_token, send_verification_email, get_verification_token, mark_token_as_used

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=EmailVerificationResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and send verification email"""
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
    
    # Create user (inactive until email verified)
    db_user = create_user(db, user, is_verified=False)
    
    # Create verification token and send email
    verification_token = create_verification_token(db, db_user.id, db_user.email)
    email_sent = send_verification_email(db_user.email, db_user.username, verification_token)
    
    return {
        "message": "Registration successful! Please check your email to verify your account.",
        "verification_sent": email_sent
    }

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
        if not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please verify your email address before logging in"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is inactive. Contact administrator."
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

@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify email address with token"""
    # Get verification token
    verification = get_verification_token(db, token)
    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Verify user email
    if verify_user_email(db, verification.user_id):
        # Mark token as used
        mark_token_as_used(db, token)
        
        # Get the verified user
        from crud import get_user_by_id
        user = get_user_by_id(db, verification.user_id)
        
        # Create access token to automatically log them in
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "is_admin": user.is_admin},
            expires_delta=access_token_expires
        )
        
        return {
            "message": "Email verified successfully! You are now logged in.",
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify email"
        )

@router.post("/resend-verification")
async def resend_verification_email(email: str, db: Session = Depends(get_db)):
    """Resend verification email"""
    user = get_user_by_email(db, email)
    if not user:
        # Don't reveal if email exists or not for security
        return {"message": "If the email exists, a verification email has been sent."}
    
    if user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )
    
    # Create new verification token and send email
    verification_token = create_verification_token(db, user.id, user.email)
    email_sent = send_verification_email(user.email, user.username, verification_token)
    
    return {"message": "Verification email sent. Please check your inbox."}

@router.get("/verify-token")
async def verify_token_endpoint(current_user = Depends(get_current_user)):
    """Verify if token is valid"""
    return {
        "valid": True,
        "user_id": current_user.id,
        "username": current_user.username,
        "is_admin": current_user.is_admin,
        "is_email_verified": current_user.is_email_verified
    }
