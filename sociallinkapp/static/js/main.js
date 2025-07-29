// Main initialization and event listeners
document.addEventListener('DOMContentLoaded', function () {
    // Determine current page type
    const isMediaPage = window.location.pathname.includes('/create-media');
    const isTextPage = window.location.pathname.includes('/create-text');
    
    // Listen for text input changes on different page types
    let textInputElement = null;
    
    if (isTextPage) {
        // Text post page
        textInputElement = document.getElementById('post-content');
    } else if (!isMediaPage) {
        // Legacy page
        textInputElement = document.querySelector('#text-form textarea');
    }
    
    if (textInputElement) {
        textInputElement.addEventListener('input', function() {
            if (typeof updateSubmitButtonState === 'function') {
                updateSubmitButtonState();
            }
            
            // Update character count for text pages
            if (isTextPage && typeof updateCharacterCount === 'function') {
                updateCharacterCount();
            }
        });
    }
    
    // Listen for caption input on media pages
    if (isMediaPage) {
        const captionTextarea = document.getElementById('caption');
        if (captionTextarea) {
            captionTextarea.addEventListener('input', function() {
                if (typeof updateSubmitButtonState === 'function') {
                    updateSubmitButtonState();
                }
            });
        }
    }

    // Initial form state update
    setTimeout(function() {
        if (typeof updateSubmitButtonState === 'function') {
            updateSubmitButtonState();
        }
        
        // Initial character count for text pages
        if (isTextPage && typeof updateCharacterCount === 'function') {
            updateCharacterCount();
        }
    }, 100);
});
