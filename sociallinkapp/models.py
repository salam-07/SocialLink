# create database model through SQLAlchemy ORM
# database related methods

from datetime import datetime
from sociallinkapp import db
import uuid

class Post(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # post ID
    post_type = db.Column(db.String(10), nullable=False)  # 'text' or 'media'
    content = db.Column(db.Text, nullable=False)  # text content or media file path
    platforms = db.Column(db.Text, nullable=False)  # JSON string of selected platforms
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # string representation of table class
    def __repr__(self):
        return f"Post(id='{self.id}', type='{self.post_type}', date='{self.date_posted}')"
    
    # make the JSON string of platforms as list
    def get_platforms_list(self):
        import json
        try:
            return json.loads(self.platforms)
        except:
            return []
    
    # convert list to JSON string
    def set_platforms_list(self, platforms_list):
        import json
        self.platforms = json.dumps(platforms_list)
