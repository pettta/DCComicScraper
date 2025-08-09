#!/usr/bin/env python3
"""
Database Setup Script for Comics Timeline Application

This script creates the main timeline database with tables for:
- Comic eras and timeline data
- Publishers information
- Comic books and series data
- Price tracking information

The script loads initial data from JSON files in this directory.
"""

import sqlite3
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Database configuration
DATABASE_NAME = "comics_timeline.db"
DATABASE_PATH = Path(__file__).parent / DATABASE_NAME

def create_timeline_tables(cursor: sqlite3.Cursor):
    """Create tables for timeline data"""
    
    # Publishers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publishers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            founded_year INTEGER,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Eras table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            publisher_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            ending_event TEXT,
            start_year INTEGER NOT NULL,
            end_year INTEGER,
            description TEXT,
            display_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (publisher_id) REFERENCES publishers (id)
        )
    ''')
    
    # Sub-eras table (for more granular timeline divisions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sub_eras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            era_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            ending_event TEXT,
            start_year INTEGER NOT NULL,
            end_year INTEGER,
            description TEXT,
            display_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (era_id) REFERENCES eras (id)
        )
    ''')
    
    # Comic series table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comic_series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            publisher_id INTEGER NOT NULL,
            era_id INTEGER,
            title TEXT NOT NULL,
            volume INTEGER DEFAULT 1,
            start_year INTEGER,
            end_year INTEGER,
            issue_count INTEGER,
            description TEXT,
            series_type TEXT DEFAULT 'ongoing', -- ongoing, limited, miniseries, oneshot
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (publisher_id) REFERENCES publishers (id),
            FOREIGN KEY (era_id) REFERENCES eras (id)
        )
    ''')
    
    # Comic issues table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comic_issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id INTEGER NOT NULL,
            issue_number TEXT NOT NULL, -- Can be "1", "1.5", "Annual 1", etc.
            title TEXT,
            publication_date DATE,
            cover_price DECIMAL(10,2),
            page_count INTEGER,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (series_id) REFERENCES comic_series (id),
            UNIQUE(series_id, issue_number)
        )
    ''')
    
    # Price tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id INTEGER NOT NULL,
            condition TEXT NOT NULL, -- Poor, Fair, Good, Very Good, Fine, Very Fine, Near Mint, Mint
            price DECIMAL(10,2) NOT NULL,
            source TEXT, -- Which website/source the price came from
            tracked_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (issue_id) REFERENCES comic_issues (id)
        )
    ''')
    
    print("✓ Created all timeline database tables")

def insert_publishers(cursor: sqlite3.Cursor):
    """Insert default publishers"""
    publishers = [
        ("DC Comics", 1934, "American comic book publisher founded by Malcolm Wheeler-Nicholson"),
        ("Marvel Comics", 1939, "American comic book publisher founded by Martin Goodman"),
        ("Image Comics", 1992, "American comic book publisher founded by several former Marvel Comics artists"),
        ("Dark Horse Comics", 1986, "American comic book and manga publisher"),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO publishers (name, founded_year, description)
        VALUES (?, ?, ?)
    ''', publishers)
    
    print("✓ Inserted default publishers")

def load_json_timeline_data(cursor: sqlite3.Cursor):
    """Load timeline data from JSON files"""
    
    # Get DC Comics publisher ID
    cursor.execute("SELECT id FROM publishers WHERE name = 'DC Comics'")
    dc_id = cursor.fetchone()[0]
    
    # Mapping of JSON files to era data
    era_files = {
        "pre_crisis.json": {
            "title": "Pre-Crisis",
            "ending_event": "Crisis on Infinite Earths",
            "start_year": 1938,
            "end_year": 1985,
            "description": "Beginning of DC Comics up to the beginning of the modern age",
            "display_order": 1
        },
        "post_crisis_pre_zero_hour.json": {
            "title": "Post-Crisis Part 1",
            "ending_event": "Zero Hour",
            "start_year": 1985,
            "end_year": 1994,
            "description": "Modern age following Crisis on Infinite Earths through Zero Hour",
            "display_order": 2
        },
        "post_crisis_pre_infinite_crisis.json": {
            "title": "Post-Crisis Part 2", 
            "ending_event": "Infinite Crisis",
            "start_year": 1994,
            "end_year": 2005,
            "description": "Zero Hour through Infinite Crisis",
            "display_order": 3
        },
        "post_crisis_pre_final_crisis.json": {
            "title": "Post-Crisis Part 3",
            "ending_event": "Final Crisis",
            "start_year": 2005,
            "end_year": 2008,
            "description": "Infinite Crisis through Final Crisis",
            "display_order": 4
        },
        "post_crisis_pre_flashpoint.json": {
            "title": "Post-Crisis Part 4",
            "ending_event": "Flashpoint",
            "start_year": 2008,
            "end_year": 2011,
            "description": "Final Crisis through Flashpoint",
            "display_order": 5
        },
        "new_52.json": {
            "title": "New 52",
            "ending_event": "DC Rebirth",
            "start_year": 2011,
            "end_year": 2016,
            "description": "The New 52 era following Flashpoint",
            "display_order": 6
        }
    }
    
    for filename, era_info in era_files.items():
        file_path = Path(__file__).parent / filename
        
        if not file_path.exists():
            print(f"⚠️  Warning: {filename} not found, skipping...")
            continue
            
        try:
            # Insert era
            cursor.execute('''
                INSERT OR IGNORE INTO eras 
                (publisher_id, title, ending_event, start_year, end_year, description, display_order)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                dc_id, 
                era_info["title"], 
                era_info["ending_event"],
                era_info["start_year"],
                era_info["end_year"],
                era_info["description"],
                era_info["display_order"]
            ))
            
            # Get the era ID
            cursor.execute('''
                SELECT id FROM eras 
                WHERE publisher_id = ? AND title = ?
            ''', (dc_id, era_info["title"]))
            era_id = cursor.fetchone()[0]
            
            # Load and process JSON data
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                
            # Process the JSON data to extract comic information
            # This will depend on the structure of your JSON files
            # For now, we'll just log that we found the file
            print(f"✓ Loaded era '{era_info['title']}' from {filename}")
            
        except Exception as e:
            print(f"✗ Error loading {filename}: {e}")
    
    print("✓ Loaded timeline data from JSON files")

def create_indexes(cursor: sqlite3.Cursor):
    """Create indexes for better query performance"""
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_eras_publisher ON eras(publisher_id)",
        "CREATE INDEX IF NOT EXISTS idx_eras_years ON eras(start_year, end_year)",
        "CREATE INDEX IF NOT EXISTS idx_sub_eras_era ON sub_eras(era_id)",
        "CREATE INDEX IF NOT EXISTS idx_comic_series_publisher ON comic_series(publisher_id)",
        "CREATE INDEX IF NOT EXISTS idx_comic_series_era ON comic_series(era_id)",
        "CREATE INDEX IF NOT EXISTS idx_comic_issues_series ON comic_issues(series_id)",
        "CREATE INDEX IF NOT EXISTS idx_price_tracking_issue ON price_tracking(issue_id)",
        "CREATE INDEX IF NOT EXISTS idx_price_tracking_date ON price_tracking(tracked_date)",
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    print("✓ Created database indexes")

def setup_database():
    """Main setup function"""
    
    print("Comics Timeline Database Setup")
    print("=" * 40)
    print(f"Database location: {DATABASE_PATH}")
    print()
    
    # Check if database already exists
    if DATABASE_PATH.exists():
        response = input(f"Database {DATABASE_NAME} already exists. Recreate? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return False
        
        # Remove existing database
        DATABASE_PATH.unlink()
        print("✓ Removed existing database")
    
    try:
        # Create database and tables
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Create all tables
        create_timeline_tables(cursor)
        
        # Insert initial data
        insert_publishers(cursor)
        load_json_timeline_data(cursor)
        
        # Create indexes
        create_indexes(cursor)
        
        # Commit changes
        conn.commit()
        
        print("\n✓ Database setup completed successfully!")
        print(f"✓ Database created at: {DATABASE_PATH}")
        print("\nNext steps:")
        print("1. Update backend configuration to use this database")
        print("2. Run the backend server to test the connection")
        print("3. Use the admin scripts to manage data")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Database setup failed: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_database()
