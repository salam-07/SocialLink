// Dashboard functionality and enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth animations to cards
    const cards = document.querySelectorAll('.bg-gray-800, .bg-gray-900');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'transform 0.2s ease-in-out';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add loading animation for quick actions
    const quickActionButtons = document.querySelectorAll('a[href*="create"], a[href*="history"], a[href*="accounts"]');
    
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.animation = 'spin 0.5s ease-in-out';
                setTimeout(() => {
                    if (icon) {
                        icon.style.animation = '';
                    }
                }, 500);
            }
        });
    });

    // Animate progress bars on page load
    const progressBars = document.querySelectorAll('.bg-blue-600, .bg-green-600');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        bar.style.transition = 'width 1s ease-in-out';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });

    // Add real-time clock to dashboard
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        const dateString = now.toLocaleDateString();
        
        // You can add this to the dashboard if needed
        console.log(`Dashboard loaded at ${timeString} on ${dateString}`);
    }

    updateClock();
    setInterval(updateClock, 60000); // Update every minute
});

// Add keyframe animation for spin
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hover-lift:hover {
        transform: translateY(-2px);
        transition: transform 0.2s ease-in-out;
    }
    
    .progress-bar-animated {
        animation: progressLoad 1s ease-in-out;
    }
    
    @keyframes progressLoad {
        from { width: 0%; }
    }
`;
document.head.appendChild(style);
