"""
Email service for Comics Timeline OAuth Proxy
Handles email verification and other email functionality
"""

import smtplib
import secrets
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from database import EmailVerification

# Email configuration (can be set via environment variables)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USERNAME)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Token expiration time (24 hours)
VERIFICATION_TOKEN_EXPIRE_HOURS = 24

def generate_verification_token() -> str:
    """Generate a secure verification token"""
    return secrets.token_urlsafe(32)

def create_verification_token(db: Session, user_id: int, email: str) -> str:
    """Create a verification token and store it in the database"""
    token = generate_verification_token()
    expires_at = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    
    # Remove any existing unused tokens for this user
    db.query(EmailVerification).filter(
        EmailVerification.user_id == user_id,
        EmailVerification.is_used == False
    ).delete()
    
    # Create new verification token
    verification = EmailVerification(
        user_id=user_id,
        token=token,
        email=email,
        expires_at=expires_at
    )
    
    db.add(verification)
    db.commit()
    db.refresh(verification)
    
    return token

def get_verification_token(db: Session, token: str) -> Optional[EmailVerification]:
    """Get verification token from database"""
    return db.query(EmailVerification).filter(
        EmailVerification.token == token,
        EmailVerification.is_used == False,
        EmailVerification.expires_at > datetime.utcnow()
    ).first()

def mark_token_as_used(db: Session, token: str) -> bool:
    """Mark verification token as used"""
    verification = get_verification_token(db, token)
    if verification:
        verification.is_used = True
        db.commit()
        return True
    return False

def create_verification_email_html(username: str, verification_url: str) -> str:
    """Create HTML email content for verification"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Verify Your Email - Comics Timeline</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1976d2; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
            .button {{ background: #1976d2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🦸‍♂️ Comics Timeline</h1>
                <h2>Email Verification</h2>
            </div>
            <div class="content">
                <h3>Welcome {username}!</h3>
                <p>Thank you for signing up for Comics Timeline! To complete your registration, please verify your email address by clicking the button below:</p>
                
                <div style="text-align: center;">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </div>
                
                <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background: #eee; padding: 10px; border-radius: 4px;">
                    {verification_url}
                </p>
                
                <p><strong>Important:</strong></p>
                <ul>
                    <li>This link will expire in 24 hours</li>
                    <li>You must verify your email before you can log in</li>
                    <li>If you didn't create this account, you can safely ignore this email</li>
                </ul>
            </div>
            <div class="footer">
                <p>Comics Timeline - Your DC Comics Reading Companion</p>
                <p>If you're having trouble, contact us or visit our help center</p>
            </div>
        </div>
    </body>
    </html>
    """

def send_verification_email(email: str, username: str, token: str) -> bool:
    """Send verification email to user"""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("⚠️  Email not configured - SMTP credentials missing")
        print(f"   For testing: Verification token is: {token}")
        print(f"   Verification URL: {FRONTEND_URL}/verify-email?token={token}")
        return True  # Return True for development/testing
    
    try:
        # Create verification URL
        verification_url = f"{FRONTEND_URL}/verify-email?token={token}"
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Verify Your Email - Comics Timeline"
        msg['From'] = FROM_EMAIL
        msg['To'] = email
        
        # Create HTML content
        html_content = create_verification_email_html(username, verification_url)
        html_part = MIMEText(html_content, 'html')
        
        # Create plain text content
        text_content = f"""
        Welcome {username}!
        
        Thank you for signing up for Comics Timeline! To complete your registration, 
        please verify your email address by visiting this link:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create this account, you can safely ignore this email.
        
        Comics Timeline - Your DC Comics Reading Companion
        """
        text_part = MIMEText(text_content, 'plain')
        
        # Attach parts
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Verification email sent to: {email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send verification email: {e}")
        print(f"   For testing: Verification token is: {token}")
        print(f"   Verification URL: {FRONTEND_URL}/verify-email?token={token}")
        return False  # Still continue with registration even if email fails
