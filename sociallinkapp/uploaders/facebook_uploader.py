"""
Facebook uploader implementation (placeholder)
"""
from .base_uploader import BaseUploader

class FacebookUploader(BaseUploader):
    """Facebook uploader implementation - Coming Soon"""
    
    def __init__(self):
        super().__init__()
        # TODO: Add Facebook API credentials from config
        
    def authenticate(self, authorization_code):
        """Facebook OAuth implementation - Coming Soon"""
        return {'success': False, 'message': 'Facebook integration coming soon'}
    
    def upload(self, post):
        """Upload post to Facebook - Coming Soon"""
        return {'success': False, 'message': 'Facebook integration coming soon'}
