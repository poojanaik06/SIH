#!/usr/bin/env python3
"""
Comprehensive user data checker for SIH crop yield prediction system
Checks both database and potential localStorage data
"""

import sqlite3
import os
import json
from datetime import datetime

def check_database_users():
    """Check users in SQLite database"""
    print("🗄️ CHECKING DATABASE USERS:")
    print("=" * 60)
    
    if not os.path.exists('sih_crop_yield.db'):
        print("❌ Database file 'sih_crop_yield.db' not found!")
        return []
    
    try:
        conn = sqlite3.connect('sih_crop_yield.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ Users table doesn't exist in database")
            return []
        
        # Get all users from database
        cursor.execute("SELECT id, email FROM users")
        db_users = cursor.fetchall()
        
        if db_users:
            print(f"✅ Found {len(db_users)} users in database:")
            for user_id, email in db_users:
                print(f"   • ID: {user_id}, Email: {email}")
        else:
            print("📭 No users found in database")
        
        conn.close()
        return db_users
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return []

def check_potential_user_files():
    """Check for potential user data files"""
    print("\\n📁 CHECKING FOR POTENTIAL USER DATA FILES:")
    print("=" * 60)
    
    # Common locations where user data might be stored
    potential_files = [
        'users.json',
        'user_data.json', 
        'registered_users.json',
        'localStorage_backup.json',
        'session_data.json'
    ]
    
    found_files = []
    
    # Check current directory
    for filename in potential_files:
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                print(f"✅ Found {filename}: {len(data) if isinstance(data, list) else 'Unknown format'} entries")
                found_files.append((filename, data))
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
    
    # Check frontend directory for any user-related files
    frontend_dir = "../frontend"
    if os.path.exists(frontend_dir):
        print("\\n🔍 Checking frontend directory...")
        for root, dirs, files in os.walk(frontend_dir):
            for file in files:
                if any(keyword in file.lower() for keyword in ['user', 'auth', 'session']):
                    file_path = os.path.join(root, file)
                    print(f"📄 Found potential user file: {file_path}")
    
    if not found_files:
        print("📭 No user data files found")
    
    return found_files

def explain_authentication_system():
    """Explain the authentication system"""
    print("\\n💡 AUTHENTICATION SYSTEM EXPLANATION:")
    print("=" * 60)
    
    print("""
🔍 Based on the code analysis, here's how your authentication works:

📱 FRONTEND AUTHENTICATION (localStorage):
   • Users register/login through the React frontend
   • User data is stored in browser's localStorage
   • Key: 'registeredUsers' - array of user objects
   • Key: 'user' - current logged-in user session
   • This is CLIENT-SIDE ONLY storage

🗄️ BACKEND AUTHENTICATION (SQLite Database):
   • FastAPI backend has proper user authentication endpoints
   • Users stored in SQLite database 'users' table
   • Passwords are properly hashed with bcrypt
   • JWT tokens for session management
   • This is SERVER-SIDE storage

❗ THE ISSUE:
   Your frontend is using localStorage (browser storage) instead of 
   calling the backend API endpoints. This means:
   
   ✅ Users can register/login in the frontend
   ❌ But they're not being saved to the database
   ❌ Database shows 0 users because frontend doesn't call backend
   
🔧 SOLUTION:
   1. Frontend should call backend API endpoints
   2. Or export localStorage data to database
   3. Or create a sync mechanism
""")

def create_user_sync_script():
    """Create a script to sync localStorage users to database"""
    print("\\n🔧 CREATING USER SYNC SOLUTION:")
    print("=" * 60)
    
    sync_script = '''
// Browser Console Script to Export localStorage Users
// Run this in your browser's developer console while on your app

function exportLocalStorageUsers() {
    const users = localStorage.getItem('registeredUsers');
    if (users) {
        const userData = JSON.parse(users);
        console.log('Found users in localStorage:', userData);
        
        // Create downloadable JSON file
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(userData, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "exported_users.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
        
        return userData;
    } else {
        console.log('No users found in localStorage');
        return [];
    }
}

// Run the export
exportLocalStorageUsers();
'''
    
    with open('export_localStorage_users.js', 'w') as f:
        f.write(sync_script)
    
    print("""
✅ Created 'export_localStorage_users.js' 

To export your localStorage users:
1. Open your app in the browser
2. Press F12 (Developer Tools)
3. Go to Console tab
4. Copy and paste the script from 'export_localStorage_users.js'
5. Press Enter to run it
6. It will download your user data as JSON

Then you can use that JSON to populate the database!
""")

def check_browser_storage_instructions():
    """Provide instructions to check browser storage"""
    print("\\n🌐 HOW TO CHECK BROWSER STORAGE:")
    print("=" * 60)
    
    print("""
To see your actual user data stored in the browser:

1. 🌐 Open your app in the browser (http://localhost:5173)
2. 🔧 Press F12 to open Developer Tools
3. 📁 Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
4. 📦 Look for "Local Storage" on the left
5. 🔍 Click on your domain (localhost:5173)
6. 👀 Look for these keys:
   • 'registeredUsers' - All registered users
   • 'user' - Currently logged in user
   • 'auth_token' - Authentication token (if any)

📊 You should see all your registered users there!
""")

def main():
    """Main function"""
    print("🌾 SIH CROP YIELD - COMPREHENSIVE USER DATA CHECKER")
    print("=" * 70)
    print(f"🕒 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check database users
    db_users = check_database_users()
    
    # Check for user data files
    user_files = check_potential_user_files()
    
    # Explain the authentication system
    explain_authentication_system()
    
    # Create sync script
    create_user_sync_script()
    
    # Browser storage instructions
    check_browser_storage_instructions()
    
    print("\\n" + "=" * 70)
    print("📋 SUMMARY:")
    print(f"   • Database users: {len(db_users)}")
    print(f"   • User data files found: {len(user_files)}")
    print("   • Authentication: Frontend localStorage + Backend SQLite")
    print("   • Issue: Frontend not connected to backend for user management")
    print("\\n✅ Check completed! Your users are likely in browser localStorage.")

if __name__ == "__main__":
    main()