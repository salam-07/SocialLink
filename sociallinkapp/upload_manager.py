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
            # Check if platform is authenticated before uploading
            if not self.is_platform_authenticated(platform):
                results[platform] = {
                    'success': False, 
                    'message': f'Not authenticated with {platform.title()}. Please connect your account first.'
                }
                continue
                
            result = self.upload_post(post, platform)
            results[platform] = result
            
            # If upload was successful and returned a URL, save it to the post
            if result['success'] and 'url' in result and result['url']:
                post.set_platform_url(platform, result['url'])
        
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
