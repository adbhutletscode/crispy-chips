document.addEventListener('DOMContentLoaded', function() {
    // Function to check if background image loaded successfully
    function checkBackgroundImageLoaded(element, fallbackClass) {
        const url = window.getComputedStyle(element).backgroundImage;
        if (url === 'none' || url === '') {
            element.classList.add(fallbackClass);
        }
    }

    // Check all dish image placeholders
    const placeholders = document.querySelectorAll('.dish-image-placeholder');
    placeholders.forEach(placeholder => {
        // Create a new image to test loading
        const img = new Image();
        img.onerror = function() {
            placeholder.style.backgroundImage = 'none';
            placeholder.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><i class="fas fa-utensils fa-3x text-muted"></i></div>';
        };
        
        // Extract the URL from the background-image
        const style = window.getComputedStyle(placeholder);
        const bgImage = style.backgroundImage;
        const url = bgImage.replace(/^url\(['"](.+)['"]\)$/, '$1');
        
        if (url && url !== 'none') {
            img.src = url;
        }
    });
});