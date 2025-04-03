// Main JavaScript file for FoodExpress

document.addEventListener('DOMContentLoaded', function() {
    // Handle image loading errors
    const images = document.querySelectorAll('img');

    images.forEach(img => {
        img.addEventListener('error', function() {
            // Replace broken images with default ones based on context
            if (this.src.includes('food')) {
                this.src = '/static/img/default-food.jpg';
            } else if (this.src.includes('restaurants')) {
                this.src = '/static/img/default-restaurant.jpg';
            } else if (this.src.includes('banner')) {
                this.src = '/static/img/default-restaurant-banner.jpg';
            } else {
                this.src = '/static/img/default-image.jpg';
            }
        });
    });
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        var flashMessages = document.querySelectorAll('.alert');
        flashMessages.forEach(function(message) {
            var alert = new bootstrap.Alert(message);
            alert.close();
        });
    }, 5000);
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();
                
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('form[action*="add_to_cart"] button[type="submit"]');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Prevent default only to show animation, then submit the form
            e.preventDefault();
            
            const form = this.closest('form');
            const originalText = this.innerHTML;
            
            // Change button text and disable
            this.innerHTML = '<i class="fas fa-check me-1"></i>Added';
            this.classList.remove('btn-primary');
            this.classList.add('btn-success');
            this.disabled = true;
            
            // After animation, submit the form
            setTimeout(() => {
                form.submit();
            }, 500);
        });
    });
    
    // Quantity increment/decrement functions
    window.incrementQuantity = function(btn) {
        const input = btn.parentNode.querySelector('.quantity-input');
        const currentValue = parseInt(input.value);
        if (currentValue < 10) {
            input.value = currentValue + 1;
        }
    };
    
    window.decrementQuantity = function(btn) {
        const input = btn.parentNode.querySelector('.quantity-input');
        const currentValue = parseInt(input.value);
        if (currentValue > 1) {
            input.value = currentValue - 1;
        }
    };
    
    // Lazy loading for images
    if ('loading' in HTMLImageElement.prototype) {
        // Browser supports native lazy loading
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Fallback for browsers that don't support lazy loading
        const lazyImageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            lazyImageObserver.observe(img);
        });
    }
    
    // Restaurant filter functionality (if on search page)
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const filter = this.dataset.filter;
                
                // Toggle active class
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Filter restaurants
                const restaurants = document.querySelectorAll('.restaurant-card');
                
                if (filter === 'all') {
                    restaurants.forEach(restaurant => {
                        restaurant.style.display = 'block';
                    });
                } else {
                    restaurants.forEach(restaurant => {
                        if (restaurant.dataset.cuisines.includes(filter)) {
                            restaurant.style.display = 'block';
                        } else {
                            restaurant.style.display = 'none';
                        }
                    });
                }
            });
        });
    }
    
    // Sort functionality (if on search page)
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortBy = this.value;
            const restaurantsContainer = document.querySelector('.restaurants-container');
            const restaurants = Array.from(document.querySelectorAll('.restaurant-card'));
            
            // Sort restaurants based on selected option
            restaurants.sort((a, b) => {
                if (sortBy === 'rating-high') {
                    return parseFloat(b.dataset.rating) - parseFloat(a.dataset.rating);
                } else if (sortBy === 'rating-low') {
                    return parseFloat(a.dataset.rating) - parseFloat(b.dataset.rating);
                } else if (sortBy === 'delivery-low') {
                    return parseFloat(a.dataset.deliveryFee) - parseFloat(b.dataset.deliveryFee);
                } else if (sortBy === 'delivery-high') {
                    return parseFloat(b.dataset.deliveryFee) - parseFloat(a.dataset.deliveryFee);
                }
            });
            
            // Re-append sorted restaurants
            restaurants.forEach(restaurant => {
                restaurantsContainer.appendChild(restaurant);
            });
        });
    }
});