import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Get values from .env file, with fallback default values only for development
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Email settings
    MAIL_SERVER = 'smtp.gmail.com'  # This is standard for Gmail
    MAIL_PORT = 587                 # Standard Gmail TLS port
    MAIL_USE_TLS = True            # Gmail requires TLS
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Scheduler settings
    SCHEDULER_API_ENABLED = True

    # Validate required environment variables
    @classmethod
    def validate_config(cls):
        required_vars = [
            'SECRET_KEY',
            'MONGO_URI',
            'MAIL_USERNAME',
            'MAIL_PASSWORD'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                f"Please check your .env file and ensure all required variables are set."
            )
