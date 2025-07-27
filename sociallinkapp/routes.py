# contains all the routes needed for application

# libraries import
from flask import render_template, url_for, redirect, flash, request, abort, session

# local imports
from sociallinkapp import app
from sociallinkapp.file_handler import handle_file_upload


# route for the landing page
@app.route('/')
@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html', heading="Dashboard", title="Dashboard")

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    uploaded_file = None
    
    if request.method == 'POST':
        # Handle file upload
        result = handle_file_upload('dropzone-file')
        
        if result['success']:
            # Store uploaded file info in session
            session['uploaded_file'] = {
                'filename': result['filename'],
                'file_path': result['file_path'],
                'original_name': request.files['dropzone-file'].filename
            }
            flash(f'File uploaded successfully!', 'success')
        else:
            flash(f'Upload failed: {result["message"]}', 'error')
        
        return redirect(url_for('create_post'))
    
    # GET request - show the form
    # Check if there's an uploaded file in session
    if 'uploaded_file' in session:
        uploaded_file = session['uploaded_file']
    
    platforms = [
        {'id': 'facebook', 'name': 'Facebook', 'icon': 'facebook.png'},
        {'id': 'x', 'name': 'X', 'icon': 'x.png'},
        {'id': 'instagram', 'name': 'Instagram', 'icon': 'instagram.png'},
        {'id': 'linkedin', 'name': 'LinkedIn', 'icon': 'linkedin.png'},
        {'id': 'threads', 'name': 'Threads', 'icon': 'threads.png'},
        {'id': 'reddit', 'name': 'Reddit', 'icon': 'reddit.png'}
    ]
    return render_template('create_post.html', heading="Publish Posts", title="Publish Posts", platforms=platforms, uploaded_file=uploaded_file)

@app.route('/remove_upload')
def remove_upload():
    """Remove uploaded file from session"""
    if 'uploaded_file' in session:
        session.pop('uploaded_file', None)
        flash('File removed successfully!', 'success')
    return redirect(url_for('create_post'))

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