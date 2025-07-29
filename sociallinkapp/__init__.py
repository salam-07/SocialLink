# initialization of Flask application.
# Do Not change this file

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Validate configuration before starting the app
try:
    Config.validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
    exit(1)

app = Flask(__name__) # create Flask app instance
app.secret_key = Config.SECRET_KEY # secret key from environment
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL # database URL from environment
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable modification tracking

db = SQLAlchemy(app) # create database instance

from sociallinkapp import models
from sociallinkapp.routes import main_routes, post_routes, auth_routes