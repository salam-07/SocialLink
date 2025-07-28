// Form submission and validation functionality
function updateSubmitButtonState() {
    const submitBtn = document.getElementById('submit-post-btn');
    const submitBtnText = document.getElementById('submit-btn-text');
    const submitStatus = document.getElementById('submit-status');
    const postTypeInput = document.getElementById('post-type-input');
    const contentInput = document.getElementById('content-input');

    // Check if all required elements exist
    if (!submitBtn || !submitBtnText || !submitStatus || !postTypeInput || !contentInput) {
        return; // Exit if any required element is missing
    }

    // Determine current post type
    const mediaUploadSection = document.getElementById('media-upload-section');
    const isMediaMode = mediaUploadSection && !mediaUploadSection.classList.contains('hidden');
    const currentPostType = isMediaMode ? 'media' : 'text';

    // Get current content based on mode
    let currentContent = '';
    if (currentPostType === 'media') {
        // Check if file is uploaded (look for uploaded file preview)
        const uploadedFilePreview = document.getElementById('uploaded-file-preview');
        const hasUploadedFile = uploadedFilePreview && !uploadedFilePreview.classList.contains('hidden');
        currentContent = hasUploadedFile ? 'media_uploaded' : '';
    } else {
        // Get text content
        const textArea = document.querySelector('#text-form textarea');
        currentContent = textArea ? textArea.value.trim() : '';
    }

    // Check if we have platforms selected and content
    const hasContent = currentContent.length > 0;
    const hasPlatforms = selectedPlatforms && selectedPlatforms.length > 0;
    const canSubmit = hasContent && hasPlatforms;

    // Update hidden form inputs
    postTypeInput.value = currentPostType;
    contentInput.value = currentContent;

    // Update platforms input with individual hidden inputs
    const finalPostForm = document.getElementById('final-post-form');
    if (finalPostForm) {
        // Clear existing platform inputs
        const existingPlatformInputs = document.querySelectorAll('input[name="selected_platforms"]');
        existingPlatformInputs.forEach(input => input.remove());

        // Add new platform inputs
        if (selectedPlatforms) {
            selectedPlatforms.forEach(platformId => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'selected_platforms';
                input.value = platformId;
                finalPostForm.appendChild(input);
            });
        }
    }

    // Update button state
    if (canSubmit) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('disabled:bg-gray-600', 'disabled:cursor-not-allowed');
        const platformCount = selectedPlatforms ? selectedPlatforms.length : 0;
        submitBtnText.textContent = `Post to ${platformCount} Platform${platformCount > 1 ? 's' : ''}`;
        submitStatus.classList.add('hidden');
    } else {
        submitBtn.disabled = true;
        submitBtn.classList.add('disabled:bg-gray-600', 'disabled:cursor-not-allowed');
        submitBtnText.textContent = 'Upload Post';
        submitStatus.classList.remove('hidden');

        // Update status message
        if (!hasPlatforms && !hasContent) {
            submitStatus.textContent = 'Please select platforms and add content before posting.';
        } else if (!hasPlatforms) {
            submitStatus.textContent = 'Please select at least one platform.';
        } else if (!hasContent) {
            if (currentPostType === 'media') {
                submitStatus.textContent = 'Please upload a file or switch to text mode.';
            } else {
                submitStatus.textContent = 'Please enter text content.';
            }
        }
    }
}
