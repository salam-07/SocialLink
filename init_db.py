# run this script to initialize the database.
# needs to be run only once

from sociallinkapp import app, db

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()

if __name__ == '__main__':
    init_db()
