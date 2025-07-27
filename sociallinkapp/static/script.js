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

    // Update button styles
    const mediaBtn = document.getElementById('media-btn');
    const textBtn = document.getElementById('text-btn');

    // Media button - active state
    mediaBtn.classList.remove('text-gray-900');
    mediaBtn.classList.add('text-blue-700');

    // Text button - inactive state
    textBtn.classList.remove('text-blue-700');
    textBtn.classList.add('text-gray-900');
}

function showText() {
    // Hide media upload section
    document.getElementById('media-upload').classList.add('hidden');
    // Show text form section
    document.getElementById('text-form').classList.remove('hidden');

    // Update button styles
    const mediaBtn = document.getElementById('media-btn');
    const textBtn = document.getElementById('text-btn');

    // Media button - inactive state
    mediaBtn.classList.remove('text-blue-700');
    mediaBtn.classList.add('text-gray-900');

    // Text button - active state
    textBtn.classList.remove('text-gray-900');
    textBtn.classList.add('text-blue-700');
}
