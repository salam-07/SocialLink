# initialization of Flask application.
# Do Not change this file

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # create Flask app instance
app.secret_key = 'your-secret-key-here-change-in-production' # secret key for development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db' # link database

db = SQLAlchemy(app) # create database instance

from sociallinkapp import routes, models