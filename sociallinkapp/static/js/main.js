// Main initialization and event listeners
document.addEventListener('DOMContentLoaded', function () {
    // Listen for text input changes
    const textArea = document.querySelector('#text-form textarea');
    if (textArea) {
        textArea.addEventListener('input', function() {
            if (typeof updateSubmitButtonState === 'function') {
                updateSubmitButtonState();
            }
        });
    }

    // Initial form state update
    setTimeout(function() {
        if (typeof updateSubmitButtonState === 'function') {
            updateSubmitButtonState();
        }
    }, 100);
});
