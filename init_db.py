#!/usr/bin/env python3
"""
Database initialization script
Run this script to create the database tables
"""

from sociallinkapp import app, db

def init_db():
    """Initialize the database with all tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Print table info
        from sociallinkapp.models import Post
        print(f"Post table created with columns: {[column.name for column in Post.__table__.columns]}")

if __name__ == '__main__':
    init_db()
