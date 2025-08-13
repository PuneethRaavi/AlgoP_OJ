// This script handles the theme toggling functionality (dark/light mode).

document.addEventListener('DOMContentLoaded', function() {
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    const themeToggleButton = document.getElementById('theme-toggle');

    // NEW: Smooth theme transition helper
    function applyThemeWithTransition() {
        // Add temporary class to enable smooth transition for all elements
        document.documentElement.classList.add('theme-transition');
        // Apply theme normally
        applyTheme();
        // Remove the transition class after animation finishes
        setTimeout(() => {
            document.documentElement.classList.remove('theme-transition');
        }, 200); // Match CSS transition duration
    }

    // This is the single source of truth for setting the theme and icons.
    function applyTheme() {
        // Check for saved theme in localStorage or user's system preference.
        const isDarkMode = localStorage.getItem('color-theme') === 'dark' || 
                           (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches);

        if (isDarkMode) {
            // If dark mode is active:
            // 1. Add 'dark' class to the <html> element.
            document.documentElement.classList.add('dark');
            // 2. Show the MOON icon.
            themeToggleDarkIcon.classList.remove('hidden');
            // 3. Hide the SUN icon.
            themeToggleLightIcon.classList.add('hidden');
        } else {
            // If light mode is active:
            // 1. Remove 'dark' class from the <html> element.
            document.documentElement.classList.remove('dark');
            // 2. Show the SUN icon.
            themeToggleLightIcon.classList.remove('hidden');
            // 3. Hide the MOON icon.
            themeToggleDarkIcon.classList.add('hidden');
        }
    }

    // Add a click event listener to the toggle button.
    themeToggleButton.addEventListener('click', function() {
        // Check the current theme and toggle it in localStorage.
        if (localStorage.getItem('color-theme') === 'dark') {
            localStorage.setItem('color-theme', 'light');
        } else {
            localStorage.setItem('color-theme', 'dark');
        }
        applyThemeWithTransition();
    });

    // Apply the correct theme as soon as the page loads.
    applyTheme();

    // Keep a reference to the timer to prevent glitches on multiple clicks
    let toastTimer;
    window.copyToClipboard = function(elementId) {
        const el = document.getElementById(elementId);
        const notification = document.getElementById('copy-alert');
        const messageSpan = document.getElementById('copy-alert-message');
        const text = el ? el.innerText : '';

        if (!notification || !messageSpan) {
        console.error('Toast notification elements not found!');
        return;
        }

        navigator.clipboard.writeText(text).then(() => {
        messageSpan.textContent = 'Copied to clipboard successfully.';
        notification.classList.add('show');

        clearTimeout(window.toastTimer);
        window.toastTimer = setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);

        }).catch(err => {
        console.error('Copy failed', err);
        messageSpan.textContent = 'Failed to copy to clipboard.';
        notification.classList.add('show');

        clearTimeout(window.toastTimer);
        window.toastTimer = setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
        });
    };
});
