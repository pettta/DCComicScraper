#!/usr/bin/env python3
"""
Data Migration Script for Comics Timeline JSON Files

This script processes the existing JSON files and loads the comic data
into the timeline database. It parses the JSON structure and creates
appropriate database records for series, issues, and price tracking.
"""

import sqlite3
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Database configuration
DATABASE_NAME = "comics_timeline.db"
DATABASE_PATH = Path(__file__).parent / DATABASE_NAME

def connect_database():
    """Connect to the timeline database"""
    if not DATABASE_PATH.exists():
        print(f"✗ Database {DATABASE_NAME} not found!")
        print("Please run setup_timeline_database.py first.")
        sys.exit(1)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_or_create_series(cursor: sqlite3.Cursor, publisher_id: int, era_id: int, 
                        series_title: str, volume: int = 1) -> int:
    """Get existing series ID or create new series"""
    
    # Check if series exists
    cursor.execute('''
        SELECT id FROM comic_series 
        WHERE publisher_id = ? AND title = ? AND volume = ?
    ''', (publisher_id, series_title, volume))
    
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # Create new series
    cursor.execute('''
        INSERT INTO comic_series (publisher_id, era_id, title, volume, series_type)
        VALUES (?, ?, ?, ?, 'ongoing')
    ''', (publisher_id, era_id, series_title, volume))
    
    return cursor.lastrowid

def parse_issue_number(issue_str: str) -> str:
    """Parse and normalize issue number strings"""
    # Handle various issue number formats
    issue_str = str(issue_str).strip()
    
    # Common patterns to normalize
    replacements = {
        '#': '',
        'Issue ': '',
        'issue ': '',
        'No. ': '',
        'no. ': ''
    }
    
    for old, new in replacements.items():
        issue_str = issue_str.replace(old, new)
    
    return issue_str

def process_json_file(file_path: Path, era_id: int, publisher_id: int, cursor: sqlite3.Cursor):
    """Process a single JSON file and extract comic data"""
    
    print(f"Processing {file_path.name}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        processed_series = 0
        processed_issues = 0
        
        # The structure will depend on your JSON format
        # This is a generic processor that handles common structures
        
        if isinstance(data, dict):
            # If data is a dictionary, look for series information
            for key, value in data.items():
                if isinstance(value, list):
                    # Assume this is a series with a list of issues
                    series_id = get_or_create_series(cursor, publisher_id, era_id, key)
                    processed_series += 1
                    
                    for item in value:
                        if isinstance(item, dict):
                            # Process individual issue
                            issue_num = item.get('issue', item.get('number', item.get('#', 'Unknown')))
                            issue_num = parse_issue_number(issue_num)
                            
                            title = item.get('title', item.get('name', ''))
                            pub_date = item.get('publication_date', item.get('date', item.get('year')))
                            cover_price = item.get('cover_price', item.get('price'))
                            
                            # Insert issue
                            cursor.execute('''
                                INSERT OR IGNORE INTO comic_issues 
                                (series_id, issue_number, title, publication_date, cover_price)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (series_id, issue_num, title, pub_date, cover_price))
                            
                            processed_issues += 1
                            
                elif isinstance(value, dict):
                    # Single series entry
                    series_id = get_or_create_series(cursor, publisher_id, era_id, key)
                    processed_series += 1
                    
                    # Check if this dict contains issue information
                    if 'issues' in value and isinstance(value['issues'], list):
                        for issue in value['issues']:
                            issue_num = issue.get('issue', issue.get('number', 'Unknown'))
                            issue_num = parse_issue_number(issue_num)
                            
                            title = issue.get('title', '')
                            pub_date = issue.get('publication_date', issue.get('date'))
                            cover_price = issue.get('cover_price', issue.get('price'))
                            
                            cursor.execute('''
                                INSERT OR IGNORE INTO comic_issues 
                                (series_id, issue_number, title, publication_date, cover_price)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (series_id, issue_num, title, pub_date, cover_price))
                            
                            processed_issues += 1
        
        elif isinstance(data, list):
            # If data is a list, assume it's a list of series or issues
            for item in data:
                if isinstance(item, dict):
                    series_name = item.get('series', item.get('title', item.get('name', 'Unknown Series')))
                    series_id = get_or_create_series(cursor, publisher_id, era_id, series_name)
                    processed_series += 1
                    
                    # Check for issue information in the item
                    issue_num = item.get('issue', item.get('number', '1'))
                    issue_num = parse_issue_number(issue_num)
                    
                    title = item.get('issue_title', item.get('title', ''))
                    pub_date = item.get('publication_date', item.get('date'))
                    cover_price = item.get('cover_price', item.get('price'))
                    
                    cursor.execute('''
                        INSERT OR IGNORE INTO comic_issues 
                        (series_id, issue_number, title, publication_date, cover_price)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (series_id, issue_num, title, pub_date, cover_price))
                    
                    processed_issues += 1
        
        print(f"  ✓ Processed {processed_series} series and {processed_issues} issues")
        
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON parsing error in {file_path.name}: {e}")
    except Exception as e:
        print(f"  ✗ Error processing {file_path.name}: {e}")

def migrate_all_json_data():
    """Migrate all JSON files to database"""
    
    print("Comics Timeline Data Migration")
    print("=" * 40)
    
    conn = connect_database()
    cursor = conn.cursor()
    
    try:
        # Get DC Comics publisher ID
        cursor.execute("SELECT id FROM publishers WHERE name = 'DC Comics'")
        result = cursor.fetchone()
        if not result:
            print("✗ DC Comics publisher not found in database!")
            print("Please run setup_timeline_database.py first.")
            return False
        
        dc_id = result[0]
        
        # Get all eras
        cursor.execute('''
            SELECT id, title FROM eras 
            WHERE publisher_id = ? 
            ORDER BY display_order
        ''', (dc_id,))
        eras = cursor.fetchall()
        
        if not eras:
            print("✗ No eras found in database!")
            print("Please run setup_timeline_database.py first.")
            return False
        
        # Map JSON files to eras
        file_era_mapping = {
            "pre_crisis.json": "Pre-Crisis",
            "post_crisis_pre_zero_hour.json": "Post-Crisis Part 1",
            "post_crisis_pre_infinite_crisis.json": "Post-Crisis Part 2",
            "post_crisis_pre_final_crisis.json": "Post-Crisis Part 3",
            "post_crisis_pre_flashpoint.json": "Post-Crisis Part 4",
            "new_52.json": "New 52"
        }
        
        # Create era lookup
        era_lookup = {title: era_id for era_id, title in eras}
        
        # Process each JSON file
        total_files = 0
        processed_files = 0
        
        for filename, era_title in file_era_mapping.items():
            file_path = Path(__file__).parent / filename
            
            if not file_path.exists():
                print(f"⚠️  Warning: {filename} not found, skipping...")
                continue
            
            total_files += 1
            
            if era_title not in era_lookup:
                print(f"⚠️  Warning: Era '{era_title}' not found for {filename}, skipping...")
                continue
            
            era_id = era_lookup[era_title]
            process_json_file(file_path, era_id, dc_id, cursor)
            processed_files += 1
        
        # Commit all changes
        conn.commit()
        
        print(f"\n✓ Migration completed!")
        print(f"✓ Processed {processed_files} of {total_files} JSON files")
        
        # Show summary statistics
        cursor.execute("SELECT COUNT(*) FROM comic_series")
        series_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM comic_issues")
        issues_count = cursor.fetchone()[0]
        
        print(f"✓ Total series in database: {series_count}")
        print(f"✓ Total issues in database: {issues_count}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def inspect_json_structure():
    """Inspect the structure of JSON files to help with migration"""
    
    print("JSON File Structure Inspector")
    print("=" * 40)
    
    json_files = list(Path(__file__).parent.glob("*.json"))
    
    if not json_files:
        print("No JSON files found in Database directory.")
        return
    
    for file_path in json_files:
        print(f"\n📄 {file_path.name}")
        print("-" * 30)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"Type: {type(data).__name__}")
            
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())[:10]}{'...' if len(data.keys()) > 10 else ''}")
                
                # Show structure of first few items
                for i, (key, value) in enumerate(data.items()):
                    if i >= 3:
                        break
                    print(f"  {key}: {type(value).__name__}")
                    if isinstance(value, list) and value:
                        print(f"    List item type: {type(value[0]).__name__}")
                        if isinstance(value[0], dict):
                            print(f"    List item keys: {list(value[0].keys())[:5]}")
                    elif isinstance(value, dict):
                        print(f"    Dict keys: {list(value.keys())[:5]}")
            
            elif isinstance(data, list):
                print(f"Length: {len(data)}")
                if data:
                    print(f"Item type: {type(data[0]).__name__}")
                    if isinstance(data[0], dict):
                        print(f"Item keys: {list(data[0].keys())}")
        
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--inspect":
        inspect_json_structure()
    else:
        migrate_all_json_data()
