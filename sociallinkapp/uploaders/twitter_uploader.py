"""
Twitter/X uploader implementation
"""
import requests
import os
import time
from requests_oauthlib import OAuth1Session
from flask import session
from config import Config
from .base_uploader import BaseUploader

class TwitterUploader(BaseUploader):
    """Twitter/X uploader implementation"""
    
    def __init__(self):
        super().__init__()
        # Get configuration from Config class
        try:
            self.consumer_key = Config.TWITTER_API_KEY
            self.consumer_secret = Config.TWITTER_API_SECRET
            self.access_token = Config.TWITTER_ACCESS_TOKEN
            self.access_token_secret = Config.TWITTER_ACCESS_TOKEN_SECRET
            
            # Validate that required credentials are available
            if not all([self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret]):
                raise ValueError("Twitter OAuth credentials not properly configured")
                
        except Exception as e:
            print(f"Warning: Twitter configuration error: {e}")
            self.consumer_key = None
            self.consumer_secret = None
            self.access_token = None
            self.access_token_secret = None
    
    @property
    def is_authenticated(self):
        """Check if Twitter is authenticated"""
        return bool(self.consumer_key and self.consumer_secret and self.access_token and self.access_token_secret)
    
    @is_authenticated.setter 
    def is_authenticated(self, value):
        """Set authentication status"""
        pass  # Authentication status is determined by credentials
    
    def authenticate(self, authorization_code=None):
        """Twitter OAuth implementation - using stored credentials"""
        if self.is_authenticated:
            return {'success': True, 'message': 'Already authenticated with Twitter'}
        else:
            return {'success': False, 'message': 'Twitter OAuth credentials not properly configured'}
    
    def upload(self, post):
        """Upload a post to Twitter"""
        if not self.is_authenticated:
            return {'success': False, 'message': 'Not authenticated with Twitter'}
        
        # Validate post content
        if not self._validate_post_content(post):
            return {'success': False, 'message': 'Invalid post content'}
        
        if post.post_type == 'text':
            # For text posts, use content directly
            return self._post_text_to_twitter(post.content)
        elif post.post_type == 'media':
            # For media posts, handle file upload and use caption
            caption = post.caption or ''
            return self._post_media_to_twitter(post.content, caption)
        else:
            return {'success': False, 'message': 'Unsupported post type'}
    
    def _get_oauth_session(self):
        """Create OAuth1Session for Twitter API requests"""
        return OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )
    
    def _post_text_to_twitter(self, text):
        """Post text content to Twitter"""
        payload = {"text": text}
        oauth = self._get_oauth_session()
        
        try:
            response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
            
            if response.status_code == 201:
                response_data = response.json()
                tweet_id = response_data.get('data', {}).get('id', '')
                
                # Construct Twitter post URL
                twitter_url = f"https://twitter.com/i/web/status/{tweet_id}" if tweet_id else None
                
                return {
                    'success': True,
                    'message': 'Post published successfully to Twitter',
                    'url': twitter_url
                }
            else:
                return {'success': False, 'message': f'Twitter API error {response.status_code}: {response.text}'}
                
        except Exception as e:
            return {'success': False, 'message': f'Twitter upload error: {str(e)}'}
    
    def _post_media_to_twitter(self, file_path, caption):
        """Post media content to Twitter"""
        # Convert relative path to absolute path
        if file_path.startswith('/static/'):
            relative_path = file_path.lstrip('/')
            absolute_file_path = os.path.join(os.getcwd(), 'sociallinkapp', relative_path)
        else:
            absolute_file_path = file_path
        
        print(f"Debug: Starting Twitter media upload for file: {absolute_file_path}")
        print(f"Debug: Caption: {caption}")
        
        # Check if file exists
        if not os.path.exists(absolute_file_path):
            return {'success': False, 'message': f'File not found: {absolute_file_path}'}
        
        # Determine if it's a video or image
        file_ext = os.path.splitext(absolute_file_path)[1].lower()
        video_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']
        
        if file_ext in video_extensions:
            return self._upload_video_to_twitter(absolute_file_path, caption)
        else:
            return self._upload_image_to_twitter(absolute_file_path, caption)
    
    def _upload_image_to_twitter(self, file_path, caption):
        """Upload image to Twitter"""
        oauth = self._get_oauth_session()
        
        try:
            # Upload media using v1.1 API (media upload)
            with open(file_path, 'rb') as file:
                files = {'media': file}
                media_response = oauth.post(
                    'https://upload.twitter.com/1.1/media/upload.json',
                    files=files
                )
            
            if media_response.status_code != 200:
                return {'success': False, 'message': f'Failed to upload image: {media_response.text}'}
            
            media_id = media_response.json()['media_id_string']
            
            # Create tweet with media using v2 API
            payload = {
                "text": caption,
                "media": {
                    "media_ids": [media_id]
                }
            }
            
            response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
            
            if response.status_code == 201:
                response_data = response.json()
                tweet_id = response_data.get('data', {}).get('id', '')
                twitter_url = f"https://twitter.com/i/web/status/{tweet_id}" if tweet_id else None
                
                return {
                    'success': True,
                    'message': 'Image posted successfully to Twitter',
                    'url': twitter_url
                }
            else:
                return {'success': False, 'message': f'Failed to create tweet: {response.text}'}
                
        except Exception as e:
            return {'success': False, 'message': f'Image upload error: {str(e)}'}
    
    def _upload_video_to_twitter(self, file_path, caption):
        """Upload video to Twitter using chunked upload"""
        try:
            # Create VideoPost instance
            video_post = TwitterVideoPost(file_path, caption, self._get_oauth_session())
            
            # Execute the upload process
            video_post.upload_init()
            video_post.upload_append()
            video_post.upload_finalize()
            result = video_post.post()
            
            return result
            
        except Exception as e:
            return {'success': False, 'message': f'Video upload error: {str(e)}'}
    
    def disconnect(self):
        """Disconnect from Twitter - clears stored session data"""
        # Note: For Twitter, we're using stored credentials, so disconnect just clears any session data
        session.pop('twitter_authenticated', None)
        return {'success': True, 'message': 'Successfully disconnected from Twitter'}


class TwitterVideoPost:
    """Helper class for Twitter video upload"""
    
    def __init__(self, file_path, caption, oauth_session):
        self.video_filename = file_path
        self.caption = caption
        self.oauth = oauth_session
        self.total_bytes = os.path.getsize(self.video_filename)
        self.media_id = None
        self.processing_info = None
        self.media_endpoint_url = 'https://upload.twitter.com/1.1/media/upload.json'
        self.post_url = 'https://api.twitter.com/2/tweets'
    
    def upload_init(self):
        """Initialize video upload"""
        print('Twitter Video Upload: INIT')
        
        request_data = {
            'command': 'INIT',
            'media_type': 'video/mp4',
            'total_bytes': self.total_bytes,
            'media_category': 'tweet_video'
        }
        
        response = self.oauth.post(url=self.media_endpoint_url, data=request_data)
        
        if response.status_code != 202:
            raise Exception(f'Init failed: {response.status_code} {response.text}')
        
        self.media_id = response.json()['media_id_string']
        print(f'Media ID: {self.media_id}')
    
    def upload_append(self):
        """Upload video in chunks"""
        segment_id = 0
        bytes_sent = 0
        
        with open(self.video_filename, 'rb') as file:
            while bytes_sent < self.total_bytes:
                chunk = file.read(4 * 1024 * 1024)  # 4MB chunks
                
                print(f'Twitter Video Upload: APPEND segment {segment_id}')
                
                files = {'media': ('chunk', chunk, 'application/octet-stream')}
                data = {
                    'command': 'APPEND',
                    'media_id': self.media_id,
                    'segment_index': segment_id
                }
                
                response = self.oauth.post(url=self.media_endpoint_url, data=data, files=files)
                
                if response.status_code not in [200, 204]:
                    raise Exception(f'Append failed: {response.status_code} {response.text}')
                
                segment_id += 1
                bytes_sent = file.tell()
                print(f'{bytes_sent} of {self.total_bytes} bytes uploaded')
        
        print('Upload chunks complete.')
    
    def upload_finalize(self):
        """Finalize video upload"""
        print('Twitter Video Upload: FINALIZE')
        
        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }
        
        response = self.oauth.post(url=self.media_endpoint_url, data=request_data)
        
        if response.status_code not in [200, 201]:
            raise Exception(f'Finalize failed: {response.status_code} {response.text}')
        
        response_data = response.json()
        self.processing_info = response_data.get('processing_info', None)
        self.check_status()
    
    def check_status(self):
        """Check video processing status"""
        if self.processing_info is None:
            return
        
        state = self.processing_info['state']
        print(f'Media processing status: {state}')
        
        if state == 'succeeded':
            return
        
        if state == 'failed':
            raise Exception('Video processing failed')
        
        check_after_secs = self.processing_info.get('check_after_secs', 5)
        print(f'Checking after {check_after_secs} seconds')
        time.sleep(check_after_secs)
        
        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }
        
        response = self.oauth.get(url=self.media_endpoint_url, params=request_params)
        
        if response.status_code != 200:
            raise Exception(f'Status check failed: {response.status_code} {response.text}')
        
        self.processing_info = response.json().get('processing_info', None)
        self.check_status()
    
    def post(self):
        """Create tweet with video"""
        payload = {
            'text': self.caption,
            'media': {
                'media_ids': [self.media_id]
            }
        }
        
        response = self.oauth.post(url=self.post_url, json=payload)
        
        if response.status_code == 201:
            response_data = response.json()
            tweet_id = response_data.get('data', {}).get('id', '')
            twitter_url = f"https://twitter.com/i/web/status/{tweet_id}" if tweet_id else None
            
            return {
                'success': True,
                'message': 'Video posted successfully to Twitter',
                'url': twitter_url
            }
        else:
            return {'success': False, 'message': f'Failed to post video tweet: {response.text}'}
