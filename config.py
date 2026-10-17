import os
from dotenv import load_dotenv

# .env फाईल मधील variables लोड करणे
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_2026')
    
    # Razorpay Keys (.env मधून येतील)
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
    
    # Database Config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sharad-ranpise-foundation.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False