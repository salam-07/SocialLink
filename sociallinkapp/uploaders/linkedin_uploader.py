"""
LinkedIn uploader implementation
"""
import requests
import os
from flask import session
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
    
    @property
    def is_authenticated(self):
        """Check if LinkedIn is authenticated by checking session"""
        return bool(session.get('linkedin_access_token') and session.get('linkedin_author_urn'))
    
    @is_authenticated.setter 
    def is_authenticated(self, value):
        """Set authentication status"""
        pass  # Authentication status is determined by session data
    
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
                access_token = token_data["access_token"]
                
                # Store in session instead of instance variable
                session['linkedin_access_token'] = access_token
                self.access_token = access_token
                
                # Get user profile
                if self._get_user_profile():
                    # Store author URN in session as well
                    session['linkedin_author_urn'] = self.author_urn
                    return {'success': True, 'message': 'Authentication successful'}
                else:
                    return {'success': False, 'message': 'Failed to get user profile'}
            else:
                return {'success': False, 'message': f'Authentication failed: {response.text}'}
        except Exception as e:
            return {'success': False, 'message': f'Authentication error: {str(e)}'}
    
    def _load_session_data(self):
        """Load authentication data from session"""
        self.access_token = session.get('linkedin_access_token')
        self.author_urn = session.get('linkedin_author_urn')
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
        # Load authentication data from session
        self._load_session_data()
        
        if not self.is_authenticated or not self.access_token or not self.author_urn:
            return {'success': False, 'message': 'Not authenticated with LinkedIn'}
        
        # Validate post content
        if not self._validate_post_content(post):
            return {'success': False, 'message': 'Invalid post content'}
        
        if post.post_type == 'text':
            # For text posts, use content directly
            return self._post_text_to_linkedin(post.content)
        elif post.post_type == 'media':
            # For media posts, handle file upload and use caption (can be empty)
            caption = post.caption or ''
            return self._post_media_to_linkedin(post.content, caption)
        else:
            return {'success': False, 'message': 'Unsupported post type'}
    
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
                # Try to extract post ID from response
                post_id = ''
                linkedin_url = None
                
                # First try to get post ID from Location header (LinkedIn API standard)
                location_header = response.headers.get('Location')
                if location_header:
                    # Location header typically contains the full URN, extract the ID
                    post_id = location_header.split('/')[-1]
                    print(f"Debug: Location header: {location_header}")
                    print(f"Debug: Extracted post_id: {post_id}")
                
                # Fallback: try to parse JSON response
                if not post_id:
                    try:
                        response_data = response.json()
                        post_id = response_data.get('id', '')
                        print(f"Debug: JSON response post_id: {post_id}")
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Could not parse LinkedIn response JSON: {e}")
                
                # Construct LinkedIn post URL if we have a post ID
                if post_id:
                    linkedin_url = f"https://www.linkedin.com/feed/update/{post_id}/"
                else:
                    linkedin_url = None
                
                return {
                    'success': True, 
                    'message': 'Post published successfully to LinkedIn',
                    'url': linkedin_url
                }
            else:
                error_msg = f"LinkedIn API error {response.status_code}: {response.text}"
                return {'success': False, 'message': error_msg}
                
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': f'Network error: {str(e)}'}
        except Exception as e:
            return {'success': False, 'message': f'Upload error: {str(e)}'}
    
    def _post_media_to_linkedin(self, file_path, caption):
        """Post media content to LinkedIn"""
        # Convert relative path to absolute path
        if file_path.startswith('/static/'):
            # Remove leading slash and convert to absolute path
            relative_path = file_path.lstrip('/')
            absolute_file_path = os.path.join(os.getcwd(), 'sociallinkapp', relative_path)
        else:
            absolute_file_path = file_path
        
        print(f"Debug: Starting media upload for file: {absolute_file_path}")
        print(f"Debug: Caption: {caption}")
        
        # Check if file exists
        if not os.path.exists(absolute_file_path):
            return {'success': False, 'message': f'File not found: {absolute_file_path}'}
        
        # Step 1: Register the upload
        upload_registration = self._register_media_upload(absolute_file_path)
        if not upload_registration['success']:
            return upload_registration
        
        print(f"Debug: Upload registered successfully, asset: {upload_registration['asset']}")
        
        # Step 2: Upload the binary file
        upload_result = self._upload_media_binary(absolute_file_path, upload_registration['upload_url'])
        if not upload_result['success']:
            return upload_result
        
        print("Debug: Binary file uploaded successfully")
        
        # Step 3: Create the share with media
        return self._create_media_share(upload_registration['asset'], caption, absolute_file_path)
    
    def _register_media_upload(self, file_path):
        """Step 1: Register media upload with LinkedIn"""
        register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Determine media type based on file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        video_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']
        
        recipe = "urn:li:digitalmediaRecipe:feedshare-video" if file_ext in video_extensions else "urn:li:digitalmediaRecipe:feedshare-image"
        
        register_body = {
            "registerUploadRequest": {
                "recipes": [recipe],
                "owner": self.author_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        
        try:
            response = requests.post(register_url, headers=headers, json=register_body)
            
            if response.status_code == 200:
                response_data = response.json()
                upload_mechanism = response_data["value"]["uploadMechanism"]
                upload_url = upload_mechanism["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
                asset = response_data["value"]["asset"]
                
                return {
                    'success': True,
                    'upload_url': upload_url,
                    'asset': asset
                }
            else:
                return {'success': False, 'message': f'Failed to register upload: {response.text}'}
                
        except Exception as e:
            return {'success': False, 'message': f'Upload registration error: {str(e)}'}
    
    def _upload_media_binary(self, file_path, upload_url):
        """Step 2: Upload binary file to LinkedIn"""
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            with open(file_path, 'rb') as file:
                response = requests.post(upload_url, headers=headers, data=file)
                
                if response.status_code in [200, 201]:
                    return {'success': True}
                else:
                    return {'success': False, 'message': f'Failed to upload file: {response.text}'}
                    
        except FileNotFoundError:
            return {'success': False, 'message': f'File not found: {file_path}'}
        except Exception as e:
            return {'success': False, 'message': f'File upload error: {str(e)}'}
    
    def _create_media_share(self, asset, caption, file_path):
        """Step 3: Create the media share"""
        share_url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Determine media category based on file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        video_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']
        media_category = "VIDEO" if file_ext in video_extensions else "IMAGE"
        
        # Get filename for title
        filename = os.path.basename(file_path)
        file_title = os.path.splitext(filename)[0]
        
        share_body = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": caption
                    },
                    "shareMediaCategory": media_category,
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": caption
                            },
                            "media": asset,
                            "title": {
                                "text": file_title
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            response = requests.post(share_url, headers=headers, json=share_body)
            
            if response.status_code == 201:
                # Extract post ID from response headers or try to parse JSON response
                post_id = ''
                linkedin_url = None
                
                # Try X-RestLi-Id header first (UGC API standard)
                post_id = response.headers.get('X-RestLi-Id', '')
                print(f"Debug: X-RestLi-Id header: {post_id}")
                
                # If no header, try to parse JSON response
                if not post_id:
                    try:
                        response_data = response.json()
                        post_id = response_data.get('id', '')
                        print(f"Debug: JSON response post_id: {post_id}")
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Could not parse media response JSON: {e}")
                
                # Construct LinkedIn post URL for UGC posts
                if post_id:
                    # UGC posts use a different URL format
                    linkedin_url = f"https://www.linkedin.com/feed/update/{post_id}/"
                    print(f"Debug: Generated media LinkedIn URL: {linkedin_url}")
                
                return {
                    'success': True,
                    'message': 'Media post published successfully to LinkedIn',
                    'url': linkedin_url
                }
            else:
                return {'success': False, 'message': f'Failed to create media share: {response.text}'}
                
        except Exception as e:
            return {'success': False, 'message': f'Media share creation error: {str(e)}'}
    
    def disconnect(self):
        """Disconnect from LinkedIn and clear authentication data"""
        # Clear session data
        session.pop('linkedin_access_token', None)
        session.pop('linkedin_author_urn', None)
        session.pop('linkedin_authenticated', None)
        
        # Clear instance variables
        self.access_token = None
        self.author_urn = None
        return {'success': True, 'message': 'Successfully disconnected from LinkedIn'}
