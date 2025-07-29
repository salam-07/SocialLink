"""
LinkedIn uploader implementation
"""
import requests
from config import Config
from .base_uploader import BaseUploader

class LinkedInUploader(BaseUploader):
    """LinkedIn uploader implementation"""
    
    def __init__(self):
        super().__init__()
        # Get configuration from Config class
        try:
            self.client_id = Config.LINKEDIN_CLIENT_ID
            self.client_secret = Config.LINKEDIN_CLIENT_SECRET
            self.redirect_uri = Config.LINKEDIN_REDIRECT_URI
            
            # Validate that required credentials are available
            if not all([self.client_id, self.client_secret, self.redirect_uri]):
                raise ValueError("LinkedIn OAuth credentials not properly configured")
                
        except Exception as e:
            print(f"Warning: LinkedIn configuration error: {e}")
            self.client_id = None
            self.client_secret = None
            self.redirect_uri = None
            
        self.author_urn = None
    
    def authenticate(self, authorization_code):
        """Exchange authorization code for access token"""
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            return {'success': False, 'message': 'LinkedIn OAuth not configured properly'}
            
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        token_data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(token_url, data=token_data)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.is_authenticated = True
                
                # Get user profile
                if self._get_user_profile():
                    return {'success': True, 'message': 'Authentication successful'}
                else:
                    return {'success': False, 'message': 'Failed to get user profile'}
            else:
                return {'success': False, 'message': f'Authentication failed: {response.text}'}
        except Exception as e:
            return {'success': False, 'message': f'Authentication error: {str(e)}'}
    
    def _get_user_profile(self):
        """Get user profile to obtain user URN"""
        if not self.access_token:
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            # Try userinfo endpoint first
            response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                user_id = user_info["sub"]
                self.author_urn = f"urn:li:person:{user_id}"
                return True
            
            # Fallback to /me endpoint
            response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
            if response.status_code == 200:
                me_data = response.json()
                user_id = me_data["id"]
                self.author_urn = f"urn:li:person:{user_id}"
                return True
                
        except Exception as e:
            print(f"Error getting user profile: {e}")
        
        return False
    
    def upload(self, post):
        """Upload a post to LinkedIn"""
        if not self.is_authenticated or not self.access_token or not self.author_urn:
            return {'success': False, 'message': 'Not authenticated with LinkedIn'}
        
        # Validate post content
        if not self._validate_post_content(post):
            return {'success': False, 'message': 'Invalid post content'}
        
        # For text posts, use content; for media posts, use caption
        post_text = post.content if post.post_type == 'text' else (post.caption or '')
        
        if not post_text:
            return {'success': False, 'message': 'No text content to post'}
        
        return self._post_text_to_linkedin(post_text)
    
    def _post_text_to_linkedin(self, text):
        """Post text content to LinkedIn"""
        post_url = "https://api.linkedin.com/rest/posts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "LinkedIn-Version": "202507",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        
        post_body = {
            "author": self.author_urn,
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED"
        }
        
        try:
            response = requests.post(post_url, headers=headers, json=post_body)
            
            if response.status_code == 201:
                # Extract post ID from response to construct LinkedIn URL
                response_data = response.json()
                post_id = response_data.get('id', '')
                
                # Construct LinkedIn post URL
                # LinkedIn post URLs follow the format: https://www.linkedin.com/feed/update/urn:li:activity:{activityId}
                linkedin_url = f"https://www.linkedin.com/feed/update/{post_id}" if post_id else None
                
                return {
                    'success': True, 
                    'message': 'Post published successfully to LinkedIn',
                    'url': linkedin_url
                }
            else:
                error_msg = f"LinkedIn API error {response.status_code}: {response.text}"
                return {'success': False, 'message': error_msg}
                
        except Exception as e:
            return {'success': False, 'message': f'Upload error: {str(e)}'}
    
    def disconnect(self):
        """Disconnect from LinkedIn and clear authentication data"""
        self.access_token = None
        self.author_urn = None
        self.is_authenticated = False
        return {'success': True, 'message': 'Successfully disconnected from LinkedIn'}
