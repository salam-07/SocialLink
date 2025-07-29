"""
Authentication routes - Platform OAuth and account management
"""
from flask import render_template, url_for, redirect, flash, request, session
from sociallinkapp import app
from sociallinkapp.upload_manager import upload_manager
from config import Config

# LinkedIn authentication route
@app.route('/auth/linkedin')
def linkedin_auth():
    # Redirect to LinkedIn OAuth with correct redirect URI
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={Config.LINKEDIN_CLIENT_ID}&redirect_uri={Config.LINKEDIN_REDIRECT_URI}&scope=openid%20profile%20w_member_social"
    return redirect(auth_url)

# LinkedIn disconnect route
@app.route('/auth/linkedin/disconnect')
def linkedin_disconnect():
    # Clear LinkedIn authentication from session
    if 'linkedin_authenticated' in session:
        session.pop('linkedin_authenticated', None)
    
    # Clear the access token from the uploader
    result = upload_manager.disconnect_platform('linkedin')
    
    if result['success']:
        flash('Successfully disconnected from LinkedIn!', 'success')
    else:
        flash('Error disconnecting from LinkedIn', 'error')
    
    return redirect(url_for('accounts'))

# account management route
@app.route('/accounts')
def accounts():
    # Check if this is a LinkedIn callback
    authorization_code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        flash(f'LinkedIn authentication error: {error}', 'error')
    elif authorization_code:
        # This is a LinkedIn callback, process the authentication
        try:
            linkedin_uploader = upload_manager.get_uploader('linkedin')
            result = linkedin_uploader.authenticate(authorization_code)
            
            if result['success']:
                flash('Successfully connected to LinkedIn!', 'success')
                session['linkedin_authenticated'] = True
            else:
                flash(f'LinkedIn authentication failed: {result["message"]}', 'error')
        except Exception as e:
            flash(f'Authentication error: {str(e)}', 'error')
    
    return render_template('accounts.html', heading="Manage Accounts", title="Manage Accounts")
