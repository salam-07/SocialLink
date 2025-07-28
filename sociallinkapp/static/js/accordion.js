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
                    if (icon) {
                        icon.classList.add('rotate-180');
                    }
                } else {
                    // Open the accordion
                    targetBody.classList.remove('hidden');
                    this.setAttribute('aria-expanded', 'true');
                    if (icon) {
                        icon.classList.remove('rotate-180');
                    }
                }
            }
        });
    });
});
