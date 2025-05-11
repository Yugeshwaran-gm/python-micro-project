from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from flask import current_app
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        
    def get_id(self):
        return str(self.user_data.get('_id'))
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

class AuthUtils:
    def __init__(self, db=None):
        # Use direct MongoDB connection
        mongo_uri = os.getenv('MONGO_URI')
        client = MongoClient(mongo_uri)
        self.db = client.timetable_db
        
    def get_user_by_email(self, email):
        try:
            print(f"Searching for user with email: {email}")
            # Get user from users collection
            user_data = self.db.users.find_one({"email": email})
            print(f"Found user data: {user_data}")
            if user_data:
                return User(user_data)
            return None
        except Exception as e:
            print(f"Error in get_user_by_email: {str(e)}")
            return None
    
    def get_user_by_id(self, user_id):
        try:
            user_data = self.db.users.find_one({"_id": ObjectId(user_id)})
            return User(user_data) if user_data else None
        except Exception as e:
            print(f"Error in get_user_by_id: {str(e)}")
            return None
    
    def create_user(self, email, password):
        try:
            user_data = {
                'email': email,
                'password': generate_password_hash(password),
                'is_admin': True
            }
            self.db.users.insert_one(user_data)
            return User(user_data)
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None
    
    def verify_password(self, user, password):
        if not user or not user.user_data:
            return False
        return check_password_hash(user.user_data['password'], password)
