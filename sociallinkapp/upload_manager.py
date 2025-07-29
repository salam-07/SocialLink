# Upload manager for handling platform uploads
from .uploaders import LinkedInUploader, TwitterUploader, FacebookUploader

class UploadManager:
    """Simple upload manager for social media platforms"""
    
    def __init__(self):
        self.platforms = {
            'linkedin': LinkedInUploader(),
            'twitter': TwitterUploader(),
            'x': TwitterUploader(),  # Alias for Twitter
            'facebook': FacebookUploader()
        }
    
    def upload_post(self, post, platform):
        """Upload a post to a specific platform"""
        if platform not in self.platforms:
            return {'success': False, 'message': f'Platform {platform} not supported'}
        
        try:
            uploader = self.platforms[platform]
            return uploader.upload(post)
        except Exception as e:
            return {'success': False, 'message': f'Upload failed: {str(e)}'}
    
    def upload_to_multiple_platforms(self, post, platforms):
        """Upload a post to multiple platforms"""
        results = {}
        for platform in platforms:
            results[platform] = self.upload_post(post, platform)
        return results
    
    def get_uploader(self, platform):
        """Get the uploader instance for a specific platform"""
        return self.platforms.get(platform)
    
    def is_platform_authenticated(self, platform):
        """Check if a platform is authenticated"""
        uploader = self.get_uploader(platform)
        return uploader.is_authenticated if uploader else False
    
    def disconnect_platform(self, platform):
        """Disconnect from a specific platform"""
        uploader = self.get_uploader(platform)
        if uploader:
            return uploader.disconnect()
        return {'success': False, 'message': f'Platform {platform} not found'}

# Global upload manager instance
upload_manager = UploadManager()
