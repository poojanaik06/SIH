#!/usr/bin/env python3
"""
Script to view all user data stored in the SIH crop yield prediction database
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

def connect_to_database():
    """Connect to the SQLite database"""
    db_path = 'sih_crop_yield.db'
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' not found!")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"✅ Connected to database: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def get_table_info(conn):
    """Get information about all tables in the database"""
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📊 DATABASE STRUCTURE:")
    print("=" * 60)
    
    for table_name in tables:
        table = table_name[0]
        print(f"\n📋 Table: {table}")
        
        # Get column information
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        print("   Columns:")
        for col in columns:
            col_name, col_type, not_null, default, pk = col[1], col[2], col[3], col[4], col[5]
            pk_str = " (PRIMARY KEY)" if pk else ""
            null_str = " NOT NULL" if not_null else ""
            default_str = f" DEFAULT {default}" if default else ""
            print(f"     • {col_name}: {col_type}{pk_str}{null_str}{default_str}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   📊 Records: {count}")

def view_table_data(conn, table_name, limit=10):
    """View data from a specific table"""
    try:
        # Use pandas for better formatting
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
        
        if len(df) == 0:
            print(f"   📭 No data in {table_name}")
            return
        
        print(f"\n📋 {table_name.upper()} DATA (showing first {min(len(df), limit)} records):")
        print("-" * 80)
        
        # Format the output nicely
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 50)
        
        print(df.to_string(index=False))
        
        if len(df) == limit:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total = cursor.fetchone()[0]
            if total > limit:
                print(f"\n   ... and {total - limit} more records")
                
    except Exception as e:
        print(f"   ❌ Error reading {table_name}: {e}")

def view_prediction_history(conn):
    """View prediction history if available"""
    cursor = conn.cursor()
    
    # Check if there's a predictions table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%prediction%';")
    pred_tables = cursor.fetchall()
    
    if pred_tables:
        print(f"\n🔮 PREDICTION HISTORY:")
        print("=" * 60)
        for table in pred_tables:
            view_table_data(conn, table[0])
    else:
        print(f"\n🔮 No prediction history tables found")

def view_user_accounts(conn):
    """View user account information"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count > 0:
            print(f"\n👥 USER ACCOUNTS:")
            print("=" * 60)
            
            # Get users (hide passwords for security)
            df = pd.read_sql_query("SELECT id, email FROM users", conn)
            print(df.to_string(index=False))
            print(f"\n   👥 Total Users: {user_count}")
        else:
            print(f"\n👥 No user accounts found")
            
    except Exception as e:
        print(f"❌ Error reading user data: {e}")

def search_recent_activity(conn):
    """Search for recent activity in the database"""
    print(f"\n📈 RECENT ACTIVITY ANALYSIS:")
    print("=" * 60)
    
    cursor = conn.cursor()
    
    # Check for recent yield data
    try:
        cursor.execute("""
            SELECT y.year, a.area_name, c.crop_name, y.yield_value, y.unit
            FROM yield_data y
            JOIN areas a ON y.area_id = a.area_id
            JOIN crops c ON y.crop_id = c.crop_id
            ORDER BY y.year DESC
            LIMIT 10
        """)
        recent_yields = cursor.fetchall()
        
        if recent_yields:
            print("\n📊 Recent Yield Records:")
            for record in recent_yields:
                year, area, crop, yield_val, unit = record
                print(f"   • {year}: {area} - {crop}: {yield_val} {unit}")
        else:
            print("   📭 No yield data found")
            
    except Exception as e:
        print(f"   ❌ Error reading yield data: {e}")

def export_data_summary(conn):
    """Export a summary of all data"""
    print(f"\n💾 DATA SUMMARY:")
    print("=" * 60)
    
    cursor = conn.cursor()
    
    # Get summary statistics
    tables_info = []
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            tables_info.append((table, count))
        except:
            tables_info.append((table, "Error"))
    
    print("📋 Table Summary:")
    for table, count in tables_info:
        print(f"   • {table:<20}: {count} records")
    
    # Calculate database size
    db_size = os.path.getsize('sih_crop_yield.db') / 1024  # KB
    print(f"\n💽 Database Size: {db_size:.1f} KB")

def main():
    """Main function to view all user data"""
    print("🌾 SIH CROP YIELD PREDICTION - USER DATA VIEWER")
    print("=" * 70)
    print(f"🕒 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        # 1. Show database structure
        get_table_info(conn)
        
        # 2. Show user accounts
        view_user_accounts(conn)
        
        # 3. Show data from each table
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        
        print(f"\n📊 TABLE DATA:")
        print("=" * 60)
        
        for table in tables:
            if table != 'users':  # Skip users table (already shown above)
                view_table_data(conn, table)
        
        # 4. Show recent activity
        search_recent_activity(conn)
        
        # 5. Show prediction history
        view_prediction_history(conn)
        
        # 6. Export summary
        export_data_summary(conn)
        
        print(f"\n✅ Data viewing completed successfully!")
        
    except Exception as e:
        print(f"❌ Error viewing data: {e}")
    
    finally:
        conn.close()
        print(f"\n🔒 Database connection closed.")

if __name__ == "__main__":
    main()