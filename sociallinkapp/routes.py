# contains all the routes needed for application

# libraries import
from flask import render_template, url_for, redirect, flash, request, abort

# local imports
from sociallinkapp import app


# route for the landing page
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create')
def create_post():
    return render_template('create_post.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')

@app.route('/help')
def help():
    return render_template('help.html')