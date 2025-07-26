// script.js for mobile nav menu

document.addEventListener('DOMContentLoaded', function () {
  const menuButton = document.getElementById('mobile-menu-button');
  const mobileMenu = document.getElementById('mobile-nav-menu');
  const overlay = document.getElementById('mobile-nav-overlay');

  if (menuButton && mobileMenu && overlay) {
    menuButton.addEventListener('click', function () {
      mobileMenu.classList.remove('-translate-x-full');
      overlay.classList.remove('hidden');
    });
    overlay.addEventListener('click', function () {
      mobileMenu.classList.add('-translate-x-full');
      overlay.classList.add('hidden');
    });
  }
});
