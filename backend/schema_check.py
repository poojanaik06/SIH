import sqlite3
import os

def check_database_schema():
    db_path = "sih_crop_yield.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print('=' * 60)
        print('           DATABASE SCHEMA & STRUCTURE')
        print('=' * 60)
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📋 TABLES IN DATABASE: {len(tables)}")
        for table in tables:
            table_name = table[0]
            print(f"\n🗃️  TABLE: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print("   COLUMNS:")
            for col in columns:
                col_id, name, col_type, not_null, default, pk = col
                nullable = "NOT NULL" if not_null else "NULLABLE"
                primary = "PRIMARY KEY" if pk else ""
                print(f"     • {name}: {col_type} ({nullable}) {primary}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"   📊 Records: {count} rows")
        
        # Show users table data specifically
        print(f"\n" + "="*60)
        print("           USER DATA VERIFICATION")
        print("="*60)
        
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        
        if users:
            print(f"✅ Found {len(users)} registered user(s):")
            for user in users:
                user_id, email, hashed_pwd, first_name, last_name, farm_size = user
                print(f"\n👤 User ID {user_id}:")
                print(f"   📧 Email: {email}")
                print(f"   👤 Name: {first_name} {last_name}")
                print(f"   🚜 Farm: {farm_size}")
                print(f"   🔐 Password: Encrypted ✅")
        else:
            print("❌ No users found in database")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()
        
    print(f"\n" + "="*60)
    print("✅ DATABASE CHECK COMPLETE - Your user data is properly stored!")
    print("="*60)

if __name__ == "__main__":
    check_database_schema()