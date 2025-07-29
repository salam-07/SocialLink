// Form submission and validation functionality
function updateSubmitButtonState() {
    const submitBtn = document.getElementById('submit-post-btn');
    const submitBtnText = document.getElementById('submit-btn-text');
    const submitStatus = document.getElementById('submit-status');
    const contentInput = document.getElementById('content-input');
    const captionInput = document.getElementById('caption-input');
    
    // Check if all required elements exist
    if (!submitBtn || !submitBtnText || !submitStatus) {
        return; // Exit if any required element is missing
    }

    // Determine current page type
    const isMediaPage = window.location.pathname.includes('/create-media');
    const isTextPage = window.location.pathname.includes('/create-text');
    
    let currentContent = '';
    let hasContent = false;
    
    if (isMediaPage) {
        // Media page: check if file is uploaded
        const uploadedFilePreview = document.getElementById('uploaded-file-preview');
        hasContent = uploadedFilePreview && !uploadedFilePreview.classList.contains('hidden');
        currentContent = hasContent ? 'media_uploaded' : '';
        
        // Update caption input if exists
        const captionTextarea = document.getElementById('caption');
        if (captionInput && captionTextarea) {
            captionInput.value = captionTextarea.value.trim();
        }
    } else if (isTextPage) {
        // Text page: check if text content exists
        const textArea = document.getElementById('post-content');
        currentContent = textArea ? textArea.value.trim() : '';
        hasContent = currentContent.length > 0;
        
        // Update content input
        if (contentInput) {
            contentInput.value = currentContent;
        }
    } else {
        // Legacy page: use old logic
        const mediaBtn = document.getElementById('media-btn');
        const isMediaMode = mediaBtn && mediaBtn.getAttribute('aria-current') === 'page';
        
        if (isMediaMode) {
            const uploadedFilePreview = document.getElementById('uploaded-file-preview');
            hasContent = uploadedFilePreview && !uploadedFilePreview.classList.contains('hidden');
            currentContent = hasContent ? 'media_uploaded' : '';
        } else {
            const textArea = document.querySelector('#text-form textarea');
            currentContent = textArea ? textArea.value.trim() : '';
            hasContent = currentContent.length > 0;
        }
        
        if (contentInput) {
            contentInput.value = currentContent;
        }
    }

    // Check if we have platforms selected and content
    const hasPlatforms = selectedPlatforms && selectedPlatforms.length > 0;
    const canSubmit = hasContent && hasPlatforms;

    // Update platforms input with individual hidden inputs
    const finalPostForm = document.getElementById('final-post-form');
    if (finalPostForm && selectedPlatforms) {
        // Clear existing platform inputs
        const existingPlatformInputs = document.querySelectorAll('input[name="selected_platforms"]');
        existingPlatformInputs.forEach(input => input.remove());

        // Add new platform inputs
        selectedPlatforms.forEach(platformId => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'selected_platforms';
            input.value = platformId;
            finalPostForm.appendChild(input);
        });
    }

    // Update button state
    if (canSubmit) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('disabled:bg-gray-600', 'disabled:cursor-not-allowed');
        const platformCount = selectedPlatforms ? selectedPlatforms.length : 0;
        
        if (isMediaPage) {
            submitBtnText.textContent = `Post to ${platformCount} Platform${platformCount > 1 ? 's' : ''}`;
        } else if (isTextPage) {
            submitBtnText.textContent = `Publish to ${platformCount} Platform${platformCount > 1 ? 's' : ''}`;
        } else {
            submitBtnText.textContent = `Post to ${platformCount} Platform${platformCount > 1 ? 's' : ''}`;
        }
        
        submitStatus.classList.add('hidden');
    } else {
        submitBtn.disabled = true;
        submitBtn.classList.add('disabled:bg-gray-600', 'disabled:cursor-not-allowed');
        
        if (isMediaPage) {
            submitBtnText.textContent = 'Post Media';
        } else if (isTextPage) {
            submitBtnText.textContent = 'Publish Post';
        } else {
            submitBtnText.textContent = 'Upload Post';
        }
        
        submitStatus.classList.remove('hidden');

        // Update status message
        if (!hasPlatforms && !hasContent) {
            if (isMediaPage) {
                submitStatus.textContent = 'Please upload media and select platforms before posting.';
            } else if (isTextPage) {
                submitStatus.textContent = 'Please write your post and select platforms before publishing.';
            } else {
                submitStatus.textContent = 'Please select platforms and add content before posting.';
            }
        } else if (!hasPlatforms) {
            submitStatus.textContent = 'Please select at least one platform.';
        } else if (!hasContent) {
            if (isMediaPage) {
                submitStatus.textContent = 'Please upload a media file.';
            } else if (isTextPage) {
                submitStatus.textContent = 'Please write your post content.';
            } else {
                submitStatus.textContent = 'Please add content before posting.';
            }
        }
    }
}

// Character count function for text posts
function updateCharacterCount() {
    const textarea = document.getElementById('post-content');
    const charCount = document.getElementById('char-count');
    
    if (textarea && charCount) {
        const count = textarea.value.length;
        charCount.textContent = `${count} character${count !== 1 ? 's' : ''}`;
        
        // Optional: Add color coding for character limits
        if (count > 280) { // Twitter limit example
            charCount.className = 'text-xs text-red-400';
        } else if (count > 240) {
            charCount.className = 'text-xs text-yellow-400';
        } else {
            charCount.className = 'text-xs text-gray-400';
        }
    }
}
