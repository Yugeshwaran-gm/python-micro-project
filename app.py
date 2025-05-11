from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import Config
from utils.auth_utils import AuthUtils
from dotenv import load_dotenv
import os
from scheduler.reminder_scheduler import ReminderScheduler

# Load environment variables
load_dotenv()

def create_app():
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    
    # Initialize MongoDB
    mongodb = PyMongo(app)
    app.mongodb = mongodb  # Store mongodb instance on app
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.timetable_routes import timetable_bp
    from routes.student_routes import student_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(student_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        auth_utils = AuthUtils()
        return auth_utils.get_user_by_id(user_id)
    
    # Initialize reminder scheduler
    scheduler = ReminderScheduler(app)
    scheduler.start()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
