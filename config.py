# Configuration settings for SocialLink application
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # LinkedIn OAuth settings
    LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_REDIRECT_URI = os.environ.get('LINKEDIN_REDIRECT_URI')
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///instance/posts.db')
    
    # Other platform settings (add as needed)
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
    
    @classmethod
    def validate_config(cls):
        """Validate that required environment variables are set"""
        required_vars = [
            'LINKEDIN_CLIENT_ID',
            'LINKEDIN_CLIENT_SECRET', 
            'LINKEDIN_REDIRECT_URI'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
