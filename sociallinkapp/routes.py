# contains all the routes needed for application

# libraries import
from flask import render_template, url_for, redirect, flash, request, abort

# local imports
from sociallinkapp import app


# route for the home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')