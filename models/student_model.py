from datetime import datetime
from bson import ObjectId
from flask import current_app
from pymongo.errors import DuplicateKeyError

class StudentModel:
    def __init__(self):
        self.db = current_app.mongodb.db
        
    def get_all_students(self):
        try:
            return list(self.db.students.find())
        except Exception as e:
            print(f"Error fetching students: {str(e)}")
            return []
    
    def get_student_by_id(self, student_id):
        try:
            return self.db.students.find_one({'_id': ObjectId(student_id)})
        except Exception as e:
            print(f"Error fetching student: {str(e)}")
            return None
    
    def create_student(self, data):
        try:
            # Check if email already exists
            existing_student = self.db.students.find_one({'email': data['email']})
            if existing_student:
                return None, "Email already exists"
            
            data['created_at'] = datetime.utcnow()
            result = self.db.students.insert_one(data)
            return result, None
        except DuplicateKeyError:
            return None, "Email already exists"
        except Exception as e:
            print(f"Error creating student: {str(e)}")
            return None, str(e)
    
    def update_student(self, student_id, data):
        try:
            # Check if email exists for other students
            existing_student = self.db.students.find_one({
                'email': data['email'],
                '_id': {'$ne': ObjectId(student_id)}
            })
            if existing_student:
                return None, "Email already exists"
            
            data['updated_at'] = datetime.utcnow()
            result = self.db.students.update_one(
                {'_id': ObjectId(student_id)},
                {'$set': data}
            )
            return result, None
        except Exception as e:
            print(f"Error updating student: {str(e)}")
            return None, str(e)
    
    def delete_student(self, student_id):
        try:
            return self.db.students.delete_one({'_id': ObjectId(student_id)})
        except Exception as e:
            print(f"Error deleting student: {str(e)}")
            return None
