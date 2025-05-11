from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

def init_database():
    # Load environment variables
    load_dotenv()
    
    try:
        # Use MONGO_URI from .env
        mongo_uri = os.getenv('MONGO_URI')
        client = MongoClient(mongo_uri)
        db = client['timetable_db']
        
        # Test connection
        db.command('ping')
        print("MongoDB connection successful!")
        
        # Create collections
        collections = db.list_collection_names()
        print(f"Existing collections: {collections}")
        
        # Initialize users collection
        if 'users' not in collections:
            # Create admin user
            admin_user = {
                'email': 'admin@time.com',
                'password': generate_password_hash('admin@123'),
                'is_admin': True
            }
            db.users.insert_one(admin_user)
            print("Created admin user (admin@time.com / admin@123)")
        else:
            print("Users collection already exists")
        
        # Initialize students collection
        if 'students' not in collections:
            db.students.insert_one({'test': 'test'})
            db.students.delete_one({'test': 'test'})
            # Create unique index on email field
            db.students.create_index('email', unique=True)
            print("Created students collection with unique email index")
        else:
            print("Students collection already exists")
        
        # Initialize timetables collection
        if 'timetables' not in collections:
            db.timetables.insert_one({'test': 'test'})
            db.timetables.delete_one({'test': 'test'})
            print("Created timetables collection")
        else:
            print("Timetables collection already exists")
        
        print("\nDatabase initialization complete!")
        print("\nYou can now log in with:")
        print("Email: admin@time.com")
        print("Password: admin@123")
        
    except Exception as e:
        print(f"Error during database initialization: {str(e)}")
        print("\nPlease check your .env file contains:")

if __name__ == "__main__":
    init_database()
