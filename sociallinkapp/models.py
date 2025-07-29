from datetime import datetime
from sociallinkapp import db
import uuid
import json

class Post(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_type = db.Column(db.String(10), nullable=False)  # 'text' or 'media'
    content = db.Column(db.Text, nullable=False)  # text content or media file path
    caption = db.Column(db.Text, nullable=True)  # optional caption for media posts
    platforms = db.Column(db.Text, nullable=False)  # JSON string of selected platforms
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Platform URLs - can be empty if not posted to that platform
    linkedin_url = db.Column(db.Text, nullable=True)
    facebook_url = db.Column(db.Text, nullable=True)
    twitter_url = db.Column(db.Text, nullable=True)
    instagram_url = db.Column(db.Text, nullable=True)
    reddit_url = db.Column(db.Text, nullable=True)
    threads_url = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f"Post(id='{self.id}', type='{self.post_type}', date='{self.date_posted}')"
    
    def get_platforms_list(self):
        """Convert platforms JSON string back to list"""
        try:
            return json.loads(self.platforms)
        except:
            return []
    
    def set_platforms_list(self, platforms_list):
        """Convert platforms list to JSON string for storage"""
        self.platforms = json.dumps(platforms_list)
    
    def get_platform_url(self, platform):
        """Get the URL for a specific platform"""
        platform_mapping = {
            'linkedin': self.linkedin_url,
            'facebook': self.facebook_url,
            'twitter': self.twitter_url,
            'x': self.twitter_url,  # X is the same as Twitter
            'instagram': self.instagram_url,
            'reddit': self.reddit_url,
            'threads': self.threads_url
        }
        return platform_mapping.get(platform) or '#'
    
    def set_platform_url(self, platform, url):
        """Set the URL for a specific platform"""
        if platform == 'linkedin':
            self.linkedin_url = url
        elif platform == 'facebook':
            self.facebook_url = url
        elif platform in ['twitter', 'x']:
            self.twitter_url = url
        elif platform == 'instagram':
            self.instagram_url = url
        elif platform == 'reddit':
            self.reddit_url = url
        elif platform == 'threads':
            self.threads_url = url
