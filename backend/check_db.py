import sqlite3
import sys
import os

# Add the app directory to Python path
sys.path.append('app')

try:
    # Connect to database
    conn = sqlite3.connect('sih_crop_yield.db')
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print('Existing tables:', [table[0] for table in tables])
    
    # If no tables exist, create them
    if not tables:
        print("No tables found. Creating tables from models...")
        from app.database import engine, Base
        from app import models
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        
        # Check again
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print('Tables after creation:', [table[0] for table in tables])
    
    # Check table schemas
    for table in ['areas', 'crops', 'yield_data', 'rainfall_data', 'temperature_data', 'pesticide_data']:
        try:
            cursor.execute(f'PRAGMA table_info({table})')
            columns = cursor.fetchall()
            print(f'\n{table} columns:')
            for col in columns:
                print(f'  {col[1]} ({col[2]})')
        except Exception as e:
            print(f'Table {table} error: {e}')
    
    conn.close()
    print("\nDatabase check completed successfully!")
    
except Exception as e:
    print(f"Database error: {e}")