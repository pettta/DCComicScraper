#!/usr/bin/env python3
"""
Script to recreate the OAuth database with the updated schema.
This will delete the existing database and create a new one with all tables.
"""

import os
import sys
from pathlib import Path

# Add the OAuth proxy directory to the Python path
oauth_proxy_dir = Path(__file__).parent.parent / "Backend" / "comics-timeline-oauth-proxy"
database_dir = Path(__file__).parent  # Current directory is Database folder
sys.path.insert(0, str(oauth_proxy_dir))

def recreate_database():
    """Recreate the database with the current schema."""
    
    # Change to the OAuth proxy directory for imports
    original_cwd = os.getcwd()
    os.chdir(oauth_proxy_dir)
    
    try:
        # Import the database module after changing directory
        from database import create_tables
        
        # Database file path - now in Database directory
        db_file = database_dir / "comics_auth.db"
        
        # Remove existing database if it exists
        if db_file.exists():
            try:
                db_file.unlink()
                print(f"✓ Removed existing database: {db_file}")
            except OSError as e:
                print(f"✗ Error removing database: {e}")
                print("Make sure the OAuth server is stopped before running this script.")
                sys.exit(1)
        
        # Create new database with current schema
        try:
            create_tables()
            print("✓ Created new database with updated schema")
            print("✓ All tables created successfully")
            print("\nThe database now includes:")
            print("  - users table with email verification support")
            print("  - email_verifications table")
            print("  - token_blacklist table")
            print("\nYou can now start the OAuth server.")
            
        except Exception as e:
            print(f"✗ Error creating database: {e}")
            sys.exit(1)
            
    finally:
        # Change back to original directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    print("OAuth Database Recreation Script")
    print("=" * 40)
    print(f"OAuth Proxy Directory: {oauth_proxy_dir}")
    print(f"Database Directory: {database_dir}")
    print(f"Database will be recreated at: {database_dir / 'comics_auth.db'}")
    print()
    
    # Confirm before proceeding
    response = input("This will delete the existing database and all user data. Continue? (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    recreate_database()
