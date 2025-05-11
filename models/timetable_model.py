from datetime import datetime
from bson import ObjectId
from flask import current_app

class TimetableModel:
    def __init__(self):
        # Get MongoDB instance directly from current_app
        self.db = current_app.mongodb.db
        
    def get_all_timetables(self):
        try:
            return list(self.db.timetables.find())
        except Exception as e:
            print(f"Error fetching timetables: {str(e)}")
            return []
    
    def get_timetable_by_id(self, timetable_id):
        try:
            return self.db.timetables.find_one({'_id': ObjectId(timetable_id)})
        except Exception as e:
            print(f"Error fetching timetable: {str(e)}")
            return None
    
    def create_timetable(self, data):
        try:
            data['created_at'] = datetime.utcnow()
            return self.db.timetables.insert_one(data)
        except Exception as e:
            print(f"Error creating timetable: {str(e)}")
            return None
    
    def update_timetable(self, timetable_id, data):
        try:
            data['updated_at'] = datetime.utcnow()
            return self.db.timetables.update_one(
                {'_id': ObjectId(timetable_id)},
                {'$set': data}
            )
        except Exception as e:
            print(f"Error updating timetable: {str(e)}")
            return None
    
    def delete_timetable(self, timetable_id):
        try:
            return self.db.timetables.delete_one({'_id': ObjectId(timetable_id)})
        except Exception as e:
            print(f"Error deleting timetable: {str(e)}")
            return None
