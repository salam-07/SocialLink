// Tab switching functionality for Media/Text posts
function showMedia() {
    // Show media upload section
    document.getElementById('media-upload-section').classList.remove('hidden');
    // Hide text form section
    document.getElementById('text-form').classList.add('hidden');
    // Show caption section for media posts
    document.getElementById('caption-section').classList.remove('hidden');

    // Update tab styles
    const mediaBtn = document.getElementById('media-btn');
    const textBtn = document.getElementById('text-btn');

    // Media tab - active state
    mediaBtn.className = 'inline-block p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active dark:text-blue-500 dark:border-blue-500';
    mediaBtn.setAttribute('aria-current', 'page');

    // Text tab - inactive state
    textBtn.className = 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300';
    textBtn.removeAttribute('aria-current');

    // Show all platforms for media
    if (typeof filterPlatforms === 'function') {
        filterPlatforms('media');
    }

    // Update form state
    if (typeof updateSubmitButtonState === 'function') {
        updateSubmitButtonState();
    }
}

function showText() {
    // Hide media upload section
    document.getElementById('media-upload-section').classList.add('hidden');
    // Show text form section
    document.getElementById('text-form').classList.remove('hidden');
    // Hide caption section for text posts
    document.getElementById('caption-section').classList.add('hidden');

    // Update tab styles
    const mediaBtn = document.getElementById('media-btn');
    const textBtn = document.getElementById('text-btn');

    // Media tab - inactive state
    mediaBtn.className = 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300';
    mediaBtn.removeAttribute('aria-current');

    // Text tab - active state
    textBtn.className = 'inline-block p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active dark:text-blue-500 dark:border-blue-500';
    textBtn.setAttribute('aria-current', 'page');

    // Show only text-compatible platforms
    if (typeof filterPlatforms === 'function') {
        filterPlatforms('text');
    }

    // Update form state
    if (typeof updateSubmitButtonState === 'function') {
        updateSubmitButtonState();
    }
}
