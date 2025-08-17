document.addEventListener('DOMContentLoaded', function() {
    const reviewContent = document.getElementById('review-content');
    const fontSizeSelector = document.getElementById('review-font-size-selector');
    
    function applyFontSize(size) {
        if (reviewContent) {
            reviewContent.style.fontSize = size;
        }
    }

    // Retrieve and apply saved font size from localStorage
    const savedFontSize = localStorage.getItem('review_font_size') || '14px';
    fontSizeSelector.value = savedFontSize;
    applyFontSize(savedFontSize);

    // Add event listener to change font size
    fontSizeSelector.addEventListener('change', function() {
        const newSize = this.value;
        applyFontSize(newSize);
        localStorage.setItem('review_font_size', newSize);
    });
});