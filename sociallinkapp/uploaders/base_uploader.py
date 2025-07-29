"""
Base uploader class for all social media platforms
"""
from abc import ABC, abstractmethod

class BaseUploader(ABC):
    """Abstract base class for all platform uploaders"""
    
    def __init__(self):
        self.access_token = None
        self.is_authenticated = False
    
    @abstractmethod
    def authenticate(self, authorization_code):
        """Exchange authorization code for access token"""
        pass
    
    @abstractmethod
    def upload(self, post):
        """Upload a post to the platform"""
        pass
    
    def disconnect(self):
        """Disconnect and clear authentication data"""
        self.access_token = None
        self.is_authenticated = False
        return {'success': True, 'message': 'Disconnected successfully'}
    
    def _validate_post_content(self, post):
        """Validate that post has required content"""
        if post.post_type == 'text':
            return bool(post.content and post.content.strip())
        elif post.post_type == 'media':
            return bool(post.content)  # File path should exist
        return False
