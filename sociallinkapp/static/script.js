// Simple sidebar toggle functionality with closing options
document.addEventListener('DOMContentLoaded', function () {
    const hamburgerBtn = document.querySelector('[data-drawer-toggle="separator-sidebar"]');
    const sidebar = document.getElementById('separator-sidebar');

    if (hamburgerBtn && sidebar) {
        // Toggle sidebar when hamburger button is clicked
        hamburgerBtn.addEventListener('click', function () {
            sidebar.classList.toggle('-translate-x-full');
        });

        // Close sidebar when clicking outside of it
        document.addEventListener('click', function (event) {
            const isClickInsideSidebar = sidebar.contains(event.target);
            const isClickOnHamburger = hamburgerBtn.contains(event.target);
            const isSidebarOpen = !sidebar.classList.contains('-translate-x-full');

            // If sidebar is open and click is outside sidebar and not on hamburger button
            if (isSidebarOpen && !isClickInsideSidebar && !isClickOnHamburger) {
                sidebar.classList.add('-translate-x-full');
            }
        });

    }
});

function showMedia() {
    // Show media upload section
    document.getElementById('media-upload').classList.remove('hidden');
    // Hide text form section
    document.getElementById('text-form').classList.add('hidden');

    // Update tab styles
    const mediaBtn = document.getElementById('media-btn');
    const textBtn = document.getElementById('text-btn');

    // Media tab - active state
    mediaBtn.className = 'inline-block p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active dark:text-blue-500 dark:border-blue-500';
    mediaBtn.setAttribute('aria-current', 'page');

    // Text tab - inactive state
    textBtn.className = 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300';
    textBtn.removeAttribute('aria-current');
}

function showText() {
    // Hide media upload section
    document.getElementById('media-upload').classList.add('hidden');
    // Show text form section
    document.getElementById('text-form').classList.remove('hidden');

    // Update tab styles
    const mediaBtn = document.getElementById('media-btn');
    const textBtn = document.getElementById('text-btn');

    // Media tab - inactive state
    mediaBtn.className = 'inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300';
    mediaBtn.removeAttribute('aria-current');

    // Text tab - active state
    textBtn.className = 'inline-block p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active dark:text-blue-500 dark:border-blue-500';
    textBtn.setAttribute('aria-current', 'page');
}

// Accordion functionality
document.addEventListener('DOMContentLoaded', function () {
    // Get all accordion buttons
    const accordionButtons = document.querySelectorAll('[data-accordion-target]');

    accordionButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Get the target accordion body
            const targetId = this.getAttribute('data-accordion-target');
            const targetBody = document.querySelector(targetId);
            const icon = this.querySelector('[data-accordion-icon]');

            if (targetBody) {
                // Toggle the accordion body
                const isExpanded = this.getAttribute('aria-expanded') === 'true';

                if (isExpanded) {
                    // Close the accordion
                    targetBody.classList.add('hidden');
                    this.setAttribute('aria-expanded', 'false');
                    icon.classList.add('rotate-180');
                } else {
                    // Open the accordion
                    targetBody.classList.remove('hidden');
                    this.setAttribute('aria-expanded', 'true');
                    icon.classList.remove('rotate-180');
                }
            }
        });
    });
});
