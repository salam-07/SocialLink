# contains all the routes needed for application

# libraries import
from flask import render_template, url_for, redirect, flash, request, abort, session
import json

# local imports
from sociallinkapp import app, db
from sociallinkapp.file_handler import handle_file_upload
from sociallinkapp.models import Post


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

@app.route('/submit_post', methods=['POST'])
def submit_post():
    """Handle final post submission to database"""
    try:
        # Get form data
        post_type = request.form.get('post_type')  # 'text' or 'media'
        content = request.form.get('content', '')
        selected_platforms = request.form.getlist('selected_platforms')
        
        # Validate required data
        if not post_type:
            flash('Post type is required!', 'error')
            return redirect(url_for('create_post'))
        
        if not selected_platforms:
            flash('Please select at least one platform!', 'error')
            return redirect(url_for('create_post'))
        
        # Handle content based on post type
        if post_type == 'media':
            # Check if there's an uploaded file in session
            if 'uploaded_file' not in session:
                flash('Please upload a file for media posts!', 'error')
                return redirect(url_for('create_post'))
            content = session['uploaded_file']['file_path']
        elif post_type == 'text':
            if not content.strip():
                flash('Text content is required for text posts!', 'error')
                return redirect(url_for('create_post'))
        
        # Create new post
        new_post = Post(
            post_type=post_type,
            content=content,
            platforms=json.dumps(selected_platforms)
        )
        
        # Save to database
        db.session.add(new_post)
        db.session.commit()
        
        # Clear session data
        session.pop('uploaded_file', None)
        
        flash(f'Post submitted successfully to {len(selected_platforms)} platform(s)!', 'success')
        return redirect(url_for('create_post'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error submitting post: {str(e)}', 'error')
        return redirect(url_for('create_post'))

@app.route('/history')
def history():
    # Get all posts from database, ordered by most recent first
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('history.html', heading="Posting History", title="Posting History", posts=posts)

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