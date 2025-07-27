from datetime import datetime
from sociallinkapp import db
import uuid

class Post(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_type = db.Column(db.String(10), nullable=False)  # 'text' or 'media'
    content = db.Column(db.Text, nullable=False)  # text content or media file path
    platforms = db.Column(db.Text, nullable=False)  # JSON string of selected platforms
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Post(id='{self.id}', type='{self.post_type}', date='{self.date_posted}')"
    
    def get_platforms_list(self):
        """Convert platforms JSON string back to list"""
        import json
        try:
            return json.loads(self.platforms)
        except:
            return []
    
    def set_platforms_list(self, platforms_list):
        """Convert platforms list to JSON string for storage"""
        import json
        self.platforms = json.dumps(platforms_list)
