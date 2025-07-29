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

# route for dashboard
@app.route('/home')
def home():
    # Get dashboard statistics
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Total posts
    total_posts = Post.query.count()
    
    # Posts this week
    week_ago = datetime.utcnow() - timedelta(days=7)
    posts_this_week = Post.query.filter(Post.date_posted >= week_ago).count()
    
    # Posts by type
    media_posts = Post.query.filter_by(post_type='media').count()
    text_posts = Post.query.filter_by(post_type='text').count()
    
    # Recent posts (last 5)
    recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    
    # Platform usage statistics
    platform_stats = {}
    all_posts = Post.query.all()
    total_platform_uses = 0
    
    for post in all_posts:
        platforms = post.get_platforms_list()
        for platform in platforms:
            platform_stats[platform] = platform_stats.get(platform, 0) + 1
            total_platform_uses += 1
    
    # Sort platforms by usage
    platform_stats = dict(sorted(platform_stats.items(), key=lambda x: x[1], reverse=True))
    
    dashboard_data = {
        'total_posts': total_posts,
        'posts_this_week': posts_this_week,
        'media_posts': media_posts,
        'text_posts': text_posts,
        'recent_posts': recent_posts,
        'platform_stats': platform_stats,
        'total_platform_uses': total_platform_uses
    }
    
    return render_template('home.html', heading="Dashboard", title="Dashboard", **dashboard_data)

#create media post route
@app.route('/create-media', methods=['GET', 'POST'])
def create_media_post():
    uploaded_file = None
    
    if request.method == 'POST':
        # Handle file upload
        result = handle_file_upload('dropzone-file')
        
        if result['success']: #if success=True
            # Store uploaded file info in session
            session['uploaded_file'] = {
                'filename': result['filename'],
                'file_path': result['file_path'],
                'original_name': request.files['dropzone-file'].filename
            }
            flash(f'File uploaded successfully!', 'success')
        else:
            flash(f'Upload failed: {result["message"]}', 'error')
    
        return redirect(url_for('create_media_post'))
    
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
    return render_template('create_media_post.html', heading="Create Media Post", title="Create Media Post", platforms=platforms, uploaded_file=uploaded_file)

#create text post route
@app.route('/create-text', methods=['GET'])
def create_text_post():
    platforms = [
        {'id': 'facebook', 'name': 'Facebook', 'icon': 'facebook.png'},
        {'id': 'x', 'name': 'X', 'icon': 'x.png'},
        {'id': 'instagram', 'name': 'Instagram', 'icon': 'instagram.png'},
        {'id': 'linkedin', 'name': 'LinkedIn', 'icon': 'linkedin.png'},
        {'id': 'threads', 'name': 'Threads', 'icon': 'threads.png'},
        {'id': 'reddit', 'name': 'Reddit', 'icon': 'reddit.png'}
    ]
    return render_template('create_text_post.html', heading="Create Text Post", title="Create Text Post", platforms=platforms)

# Remove uploaded file route
@app.route('/remove_upload')
def remove_upload():
    if 'uploaded_file' in session:
        session.pop('uploaded_file', None)
        flash('File removed successfully!', 'success')
    return redirect(url_for('create_media_post'))

# Submit media post to database
@app.route('/submit_media_post', methods=['POST'])
def submit_media_post():
    try:
        # Get form data
        caption = request.form.get('caption', '').strip()
        selected_platforms = request.form.getlist('selected_platforms')
        
        # Validate required data
        if not selected_platforms:
            flash('Please select at least one platform!', 'error')
            return redirect(url_for('create_media_post'))
        
        # Check if there's an uploaded file in session
        if 'uploaded_file' not in session:
            flash('Please upload a file for media posts!', 'error')
            return redirect(url_for('create_media_post'))
        
        content = session['uploaded_file']['file_path']
        
        # Create new post
        new_post = Post(
            post_type='media',
            content=content,
            caption=caption if caption else None,
            platforms=json.dumps(selected_platforms)
        )
        
        # Save to database
        db.session.add(new_post)
        db.session.commit()
        
        # Clear session data
        session.pop('uploaded_file', None)
        
        flash(f'Media post submitted successfully to {len(selected_platforms)} platform(s)!', 'success')
        return redirect(url_for('create_media_post'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error submitting media post: {str(e)}', 'error')
        return redirect(url_for('create_media_post'))

# Submit text post to database
@app.route('/submit_text_post', methods=['POST'])
def submit_text_post():
    try:
        # Get form data
        content = request.form.get('content', '').strip()
        selected_platforms = request.form.getlist('selected_platforms')
        
        # Validate required data
        if not selected_platforms:
            flash('Please select at least one platform!', 'error')
            return redirect(url_for('create_text_post'))
        
        if not content:
            flash('Text content is required for text posts!', 'error')
            return redirect(url_for('create_text_post'))
        
        # Create new post
        new_post = Post(
            post_type='text',
            content=content,
            caption=None,  # No caption for text posts
            platforms=json.dumps(selected_platforms)
        )
        
        # Save to database
        db.session.add(new_post)
        db.session.commit()
        
        flash(f'Text post submitted successfully to {len(selected_platforms)} platform(s)!', 'success')
        return redirect(url_for('create_text_post'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error submitting text post: {str(e)}', 'error')
        return redirect(url_for('create_text_post'))

# post history route
@app.route('/history')
def history():
    posts = Post.query.order_by(Post.date_posted.desc()).all() # order by date
    return render_template('history.html', heading="Posting History", title="Posting History", posts=posts)

# account management route
@app.route('/accounts')
def accounts():
    return render_template('accounts.html', heading="Manage Accounts", title="Manage Accounts")

# help page route
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