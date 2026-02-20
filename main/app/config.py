import os
from datetime import timedelta


class Config:
    # Base configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/workout_db')
    
    # Flask configuration
    DEBUG = os.environ.get('FLASK_ENV') == 'development'