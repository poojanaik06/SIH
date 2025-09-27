from app.database import SessionLocal
from app.models import User

def check_database_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print('=== USER DATABASE CONTENTS ===')
        if users:
            for user in users:
                print(f'ID: {user.id}')
                print(f'Email: {user.email}')
                print(f'First Name: {user.first_name}')
                print(f'Last Name: {user.last_name}')
                print(f'Farm Size: {user.farm_size}')
                print('---')
            print(f'Total users in database: {len(users)}')
        else:
            print('No users found in database')
    finally:
        db.close()

if __name__ == "__main__":
    check_database_users()