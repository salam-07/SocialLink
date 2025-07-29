"""
Post-related routes - Creating, submitting, and viewing posts
"""
from flask import render_template, url_for, redirect, flash, request, session
import json
from sociallinkapp import app, db
from sociallinkapp.file_handler import handle_file_upload
from sociallinkapp.models import Post
from sociallinkapp.upload_manager import upload_manager

# create media post route
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

# create text post route
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
        
        # Save to database for history
        db.session.add(new_post)
        db.session.commit()
        
        # Clear session data
        session.pop('uploaded_file', None)
        
        # Immediately upload to platforms
        upload_results = upload_manager.upload_to_multiple_platforms(new_post, selected_platforms)
        
        # Save any platform URLs that were returned
        try:
            db.session.commit()  # Commit the URL updates
        except Exception as e:
            print(f"Error saving platform URLs: {e}")
        
        # Process upload results
        successful_uploads = []
        failed_uploads = []
        
        for platform, result in upload_results.items():
            if result['success']:
                successful_uploads.append(platform)
            else:
                failed_uploads.append(f"{platform}: {result['message']}")
        
        if successful_uploads:
            flash(f'Successfully posted to: {", ".join(successful_uploads)}', 'success')
        
        if failed_uploads:
            for error in failed_uploads:
                flash(f'Failed to post - {error}', 'warning')
        
        return redirect(url_for('create_media_post'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error posting: {str(e)}', 'error')
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
        
        # Save to database for history
        db.session.add(new_post)
        db.session.commit()
        
        # Immediately upload to platforms
        upload_results = upload_manager.upload_to_multiple_platforms(new_post, selected_platforms)
        
        # Save any platform URLs that were returned
        try:
            db.session.commit()  # Commit the URL updates
        except Exception as e:
            print(f"Error saving platform URLs: {e}")
        
        # Process upload results
        successful_uploads = []
        failed_uploads = []
        
        for platform, result in upload_results.items():
            if result['success']:
                successful_uploads.append(platform)
            else:
                failed_uploads.append(f"{platform}: {result['message']}")
        
        if successful_uploads:
            flash(f'Successfully posted to: {", ".join(successful_uploads)}', 'success')
        
        if failed_uploads:
            for error in failed_uploads:
                flash(f'Failed to post - {error}', 'warning')
        
        return redirect(url_for('create_text_post'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error posting: {str(e)}', 'error')
        return redirect(url_for('create_text_post'))

# post history route
@app.route('/history')
def history():
    posts = Post.query.order_by(Post.date_posted.desc()).all() # order by date
    return render_template('history.html', heading="Post History", title="Post History", posts=posts)

# post detail route
@app.route('/post/<post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', heading="Post Details", title="Post Details", post=post)
