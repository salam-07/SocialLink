// Platform selection functionality
let selectedPlatforms = [];

function togglePlatform(platformId, platformName) {
    const platformCard = document.querySelector(`[data-platform-id="${platformId}"]`);
    const selectedPlatformsDisplay = document.getElementById('selected-platforms');

    if (selectedPlatforms.includes(platformId)) {
        // Remove platform from selection
        selectedPlatforms = selectedPlatforms.filter(id => id !== platformId);
        platformCard.classList.remove('bg-blue-600', 'border-blue-500');
        platformCard.classList.add('bg-gray-800', 'border-gray-600');
    } else {
        // Add platform to selection
        selectedPlatforms.push(platformId);
        platformCard.classList.remove('bg-gray-800', 'border-gray-600');
        platformCard.classList.add('bg-blue-600', 'border-blue-500');
    }

    // Update the display text
    updateSelectedPlatformsDisplay();
}

function updateSelectedPlatformsDisplay() {
    const selectedPlatformsDisplay = document.getElementById('selected-platforms');

    if (selectedPlatformsDisplay) {
        if (selectedPlatforms.length === 0) {
            selectedPlatformsDisplay.textContent = 'None';
            selectedPlatformsDisplay.className = 'text-gray-400';
        } else {
            // Get platform names from the selected IDs
            const platformNames = selectedPlatforms.map(id => {
                const card = document.querySelector(`[data-platform-id="${id}"]`);
                return card ? card.getAttribute('data-platform-name') : id;
            });

            selectedPlatformsDisplay.textContent = platformNames.join(', ');
            selectedPlatformsDisplay.className = 'text-blue-400';
        }
    }

    // Update form validation
    if (typeof updateSubmitButtonState === 'function') {
        updateSubmitButtonState();
    }
}

// Platform filtering function
function filterPlatforms(mode) {
    // Define which platforms are available for text posts
    const textOnlyPlatforms = ['x', 'reddit', 'threads', 'linkedin'];

    // Get all platform cards
    const platformCards = document.querySelectorAll('.platform-card');

    platformCards.forEach(card => {
        const platformId = card.getAttribute('data-platform-id');

        if (mode === 'text') {
            // Show only text-compatible platforms
            if (textOnlyPlatforms.includes(platformId)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
                // Remove from selection if it was selected and now hidden
                if (selectedPlatforms.includes(platformId)) {
                    selectedPlatforms = selectedPlatforms.filter(id => id !== platformId);
                }
            }
        } else {
            // Show all platforms for media
            card.style.display = 'block';
        }
    });

    // Update the selected platforms display
    updateSelectedPlatformsDisplay();
}
