# handle file uploads

import os
import uuid
from flask import current_app, flash, request
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = 'sociallinkapp/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'mp4', 'mov', 'avi', 'webm'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    # returns True if the file has an allowed extension
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    # get the file extension from the filename
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''

def generate_unique_filename(original_filename):
    #create a unique random filename for safety purposes

    # Get the file extension
    extension = get_file_extension(original_filename)

    # Generate a unique identifier
    unique_id = str(uuid.uuid4())
    
    # Create new filename with UUID and original extension
    if extension:
        new_filename = f"{unique_id}.{extension}"
    else:
        new_filename = unique_id
    
    return new_filename

def ensure_upload_directory():
    # create upload directory where it is not available
    upload_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        print(f"Created upload directory: {upload_path}")
    return upload_path

def validate_file_size(file):
    # valid file size, Max 16MB. Returns True if Valid

    # Get file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    return file_size <= MAX_FILE_SIZE # return bool

def handle_file_upload(file_key='file'):
    # call functions and handle file input. Returns dict

    result = {
        'success': False,
        'message': '',
        'filename': None,
        'file_path': None
    }
    
    try:
        # Check if file is in request
        if file_key not in request.files:
            result['message'] = 'No file part in request'
            return result
        
        file = request.files[file_key]
        
        # Check if file was selected
        if file.filename == '':
            result['message'] = 'No file selected'
            return result
        
        # Validate file extension
        if not allowed_file(file.filename):
            result['message'] = f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            return result
        
        # Validate file size
        if not validate_file_size(file):
            result['message'] = f'File size exceeds maximum limit of {MAX_FILE_SIZE // (1024*1024)}MB'
            return result
        
        # Ensure upload directory exists
        upload_path = ensure_upload_directory()
        
        # Generate secure filename
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        
        # Save file
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        # Success
        result['success'] = True
        result['message'] = 'File uploaded successfully. Select Platforms to post.'
        result['filename'] = unique_filename
        result['file_path'] = f'/static/uploads/{unique_filename}'
        
        print(f"File uploaded successfully: {unique_filename}")
        
    except Exception as e:
        result['message'] = f'Upload failed: {str(e)}'
        print(f"Upload error: {str(e)}")
    
    return result

def delete_uploaded_file(filename):
    # perform deletion of file upload. Return bool for success
    try:
        upload_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
        file_path = os.path.join(upload_path, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted successfully: {filename}")
            return True
        else:
            print(f"File not found: {filename}")
            return False
            
    except Exception as e:
        print(f"Error deleting file {filename}: {str(e)}")
        return False

def get_file_info(filename):
    # function to get file information. Return Dictionary
    try:
        upload_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
        file_path = os.path.join(upload_path, filename)
        
        if os.path.exists(file_path):
            file_stats = os.stat(file_path)
            return {
                'filename': filename,
                'size': file_stats.st_size,
                'size_mb': round(file_stats.st_size / (1024*1024), 2),
                'extension': get_file_extension(filename),
                'path': f'/static/uploads/{filename}',
                'exists': True
            }
        else:
            return {'exists': False}
            
    except Exception as e:
        print(f"Error getting file info for {filename}: {str(e)}")
        return {'exists': False, 'error': str(e)}
