# contains all the routes needed for application

# libraries import
from flask import render_template, url_for, redirect, flash, request, abort

# local imports
from sociallinkapp import app


# route for the landing page
@app.route('/')
@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html', heading="Dashboard", title="Dashboard")

@app.route('/create')
def create_post():
    platforms = [
        {'id': 'facebook', 'name': 'Facebook', 'icon': 'facebook.png'},
        {'id': 'x', 'name': 'X', 'icon': 'x.png'},
        {'id': 'instagram', 'name': 'Instagram', 'icon': 'instagram.png'},
        {'id': 'linkedin', 'name': 'LinkedIn', 'icon': 'linkedin.png'},
        {'id': 'threads', 'name': 'Threads', 'icon': 'threads.png'},
        {'id': 'reddit', 'name': 'Reddit', 'icon': 'reddit.png'}
    ]
    return render_template('create_post.html', heading="Publish Posts", title="Publish Posts", platforms=platforms)

@app.route('/history')
def history():
    return render_template('history.html', heading="Posting History", title="Posting History")

@app.route('/accounts')
def accounts():
    return render_template('accounts.html', heading="Manage Accounts", title="Manage Accounts")

@app.route('/help')
def help():
    faq_data = [
        {
            'id': 1,
            'question': 'What is SocialLink?',
            'answer': [
                'SocialLink is a powerful social media management platform that allows you to create, schedule, and manage posts across multiple social media platforms from one centralized dashboard.',
                'With SocialLink, you can streamline your social media workflow, save time, and maintain a consistent online presence across all your social media accounts.'
            ]
        },
        {
            'id': 2,
            'question': 'What is SocialLink?',
            'answer': [
                'SocialLink is a powerful social media management platform that allows you to create, schedule, and manage posts across multiple social media platforms from one centralized dashboard.',
                'With SocialLink, you can streamline your social media workflow, save time, and maintain a consistent online presence across all your social media accounts.'
            ]
        }
    ]
    return render_template('help.html', heading="Help", title="Help", faq_data=faq_data)