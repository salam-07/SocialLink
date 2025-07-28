// Sidebar toggle functionality with closing options
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
