#!/usr/bin/env python3
"""
Create Admin User Script for Comics Timeline OAuth Proxy

This script creates an initial admin user in the OAuth proxy database.
Run this script to set up your first admin account.
"""

import argparse
import getpass
import sys
import os
from pathlib import Path

# Store original working directory for cleanup
original_cwd = os.getcwd()

# Add the OAuth proxy directory to Python path
oauth_proxy_path = Path(__file__).parent.parent / "Backend" / "comics-timeline-oauth-proxy"
sys.path.insert(0, str(oauth_proxy_path))

# Note: Database is now stored in the Database directory (current directory)
# but we still need to import from the OAuth proxy directory

try:
    from database import get_db, create_tables, User
    from crud import get_user_by_username, get_user_by_email, create_user
    from schemas import UserCreate
    from auth import get_password_hash
    from sqlalchemy.orm import Session
except ImportError as e:
    print(f"❌ Error importing OAuth proxy modules: {e}")
    print("   Make sure you're running this from the Database directory and the OAuth proxy is set up correctly.")
    os.chdir(original_cwd)  # Restore original directory
    sys.exit(1)
finally:
    # Note: We keep the working directory changed for database operations
    pass

def create_admin_user(username: str, email: str, password: str) -> bool:
    """Create an admin user in the database"""
    
    # Ensure database tables exist
    print("🔧 Creating database tables...")
    create_tables()
    
    # Get database session
    db = next(get_db())
    
    try:
        # Check if user already exists
        existing_user = get_user_by_username(db, username)
        if existing_user:
            print(f"❌ User '{username}' already exists!")
            return False
        
        existing_email = get_user_by_email(db, email)
        if existing_email:
            print(f"❌ Email '{email}' is already registered!")
            return False
        
        # Create the user using CRUD function
        user_data = UserCreate(
            username=username,
            email=email,
            password=password
        )
        
        user = create_user(db, user_data, is_verified=True)  # Admin users are pre-verified
        
        # Make the user an admin by directly updating the database
        user.is_admin = True
        user.is_active = True
        user.is_email_verified = True  # Admin users have verified emails
        db.commit()
        db.refresh(user)
        
        print(f"✅ Successfully created admin user: {username}")
        print(f"   Email: {email}")
        print(f"   Admin: Yes")
        print(f"   Active: Yes")
        print(f"   User ID: {user.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def validate_username(username: str) -> bool:
    """Validate username format"""
    if len(username) < 3:
        print("❌ Username must be at least 3 characters long")
        return False
    if len(username) > 50:
        print("❌ Username must be less than 50 characters")
        return False
    if not username.replace("_", "").replace("-", "").isalnum():
        print("❌ Username can only contain letters, numbers, underscores, and hyphens")
        return False
    return True

def validate_email(email: str) -> bool:
    """Basic email validation"""
    if "@" not in email or "." not in email.split("@")[-1]:
        print("❌ Please enter a valid email address")
        return False
    return True

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        print("❌ Password must be at least 8 characters long")
        return False
    if len(password) > 100:
        print("❌ Password must be less than 100 characters")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Create an admin user for the Comics Timeline OAuth Proxy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_admin_user.py
  python create_admin_user.py -u admin -e admin@example.com
  python create_admin_user.py --username myAdmin --email admin@mysite.com --password
        """
    )
    
    parser.add_argument('-u', '--username', 
                        help='Admin username (will prompt if not provided)')
    parser.add_argument('-e', '--email',
                        help='Admin email address (will prompt if not provided)')
    parser.add_argument('-p', '--password', action='store_true',
                        help='Prompt for password (recommended for security)')
    parser.add_argument('--password-value',
                        help='Password value (NOT RECOMMENDED - use --password instead)')
    
    args = parser.parse_args()
    
    print("="*60)
    print("COMICS TIMELINE OAUTH PROXY - ADMIN USER CREATION")
    print("="*60)
    
    # Get username
    username = args.username
    while not username or not validate_username(username):
        username = input("Enter admin username: ").strip()
    
    # Get email
    email = args.email
    while not email or not validate_email(email):
        email = input("Enter admin email: ").strip()
    
    # Get password
    password = args.password_value
    if args.password or not password:
        while True:
            password = getpass.getpass("Enter admin password: ")
            if validate_password(password):
                confirm_password = getpass.getpass("Confirm admin password: ")
                if password == confirm_password:
                    break
                else:
                    print("❌ Passwords do not match. Please try again.")
            else:
                print("Please enter a stronger password.")
    else:
        if not validate_password(password):
            print("❌ Password provided via --password-value is not strong enough")
            sys.exit(1)
    
    print("\n📋 Creating admin user with the following details:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Admin privileges: Yes")
    
    # Confirm creation
    confirm = input("\nProceed with admin user creation? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Admin user creation cancelled.")
        sys.exit(0)
    
    # Create the admin user
    success = create_admin_user(username, email, password)
    
    if success:
        print("\n🎉 Admin user created successfully!")
        print("\nYou can now use this admin account to:")
        print("   • Log into the Comics Timeline application")
        print("   • Use the admin_user_manager.py script")
        print("   • Access admin endpoints in the OAuth proxy")
        print("\nNext steps:")
        print("   1. Start the OAuth proxy: cd ../Backend/comics-timeline-oauth-proxy && python local_setup.py")
        print(f"   2. Test admin login: python admin_user_manager.py -u {username} -p [password]")
        print(f"\n📁 Database created")
    else:
        print("\n❌ Failed to create admin user. Please check the errors above.")
        sys.exit(1)
    
    # Restore original working directory
    os.chdir(original_cwd)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user")
        # Restore original working directory on exit
        try:
            os.chdir(original_cwd)
        except:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        # Restore original working directory on exit
        try:
            os.chdir(original_cwd)
        except:
            pass
        sys.exit(1)
