# Crispy Chips Web Application

A Flask-based e-commerce web application for selling chips online. This application includes product browsing, shopping cart functionality, checkout process, an admin panel for product management, interactive chatbot, and informational pages.

## Features

- **Product Catalog**: Browse through a variety of chip products
- **Product Details**: View detailed information about each product
- **Shopping Cart**: Add products to cart, update quantities, and remove items
- **Checkout Process**: Simple checkout form for placing orders
- **Admin Panel**: Manage products (add, edit, delete)
- **Interactive Chatbot**: Customer support chatbot for immediate assistance
- **About Us & Contact Pages**: Company information and contact form
- **Responsive Design**: Works on desktop and mobile devices

## Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/crispy-chips.git
   cd crispy-chips
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python run.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Production Deployment

For detailed instructions on deploying this application to a production environment, please refer to the [Production Deployment Guide](PRODUCTION_DEPLOYMENT.md).

## Project Structure

```
crispy_chips/
│
├── app.py                      # Main Flask application with all routes and logic
├── run.py                      # Script to run the application
├── requirements.txt            # List of Python dependencies
├── README.md                   # Project documentation
├── PRODUCTION_DEPLOYMENT.md    # Production deployment guide
├── .gitignore                  # Git ignore file
│
├── data/                       # Data storage directory
│   └── products.json           # JSON file storing product information
│
├── static/                     # Static files directory
│   ├── css/
│   │   ├── style.css           # Main CSS styles for the website
│   │   └── chatbot.css         # CSS styles for the chatbot feature
│   │
│   ├── js/
│   │   ├── main.js             # Main JavaScript functionality
│   │   └── chatbot.js          # JavaScript for chatbot functionality
│   │
│   └── uploads/                # Directory for storing product images
│       └── .gitkeep            # Empty file to ensure directory is tracked in git
│
├── templates/                  # HTML templates directory
│   ├── base.html               # Base template with common layout elements
│   ├── index.html              # Homepage with product listing
│   ├── product_detail.html     # Product details page
│   ├── cart.html               # Shopping cart page
│   ├── checkout.html           # Checkout page
│   ├── about.html              # About Us page
│   ├── contact.html            # Contact Us page
│   │
│   └── admin/                  # Admin templates directory
│       ├── index.html          # Admin dashboard
│       ├── add_product.html    # Form for adding new products
│       └── edit_product.html   # Form for editing existing products
│
└── instance/                   # Instance-specific data
    └── database.db             # SQLite database (created at runtime)
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Storage**: JSON files
- **Interactive Features**: AJAX, Fetch API
- **Animations**: Animate.css
- **Icons**: Font Awesome 5

## Performance Optimization

The application includes several performance optimizations:

1. **Static Asset Caching**: CSS and JavaScript files are cached with appropriate headers
2. **Lazy Loading**: Images are lazy-loaded to improve initial page load time
3. **Minified Resources**: Production deployment should use minified CSS and JS
4. **Responsive Images**: Images are optimized for different screen sizes

## Browser Compatibility

The application is tested and compatible with:
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest version)
- Mobile browsers (iOS Safari, Android Chrome)

## Development Workflow

To contribute to this project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Testing

To run tests:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run tests
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support and Contact

For support or inquiries, please contact:
- Technical Support: support@crispychips.com
- Development Team: dev@crispychips.com

## Acknowledgements

- Bootstrap for the responsive design components
- Font Awesome for the icons
- Animate.css for animations
- Unsplash for stock photography

## Project Structure

```
crispy_chips/
│
├── app.py                      # Main Flask application with all routes and logic
├── run.py                      # Script to run the application
├── requirements.txt            # List of Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore file
│
├── data/                       # Data storage directory
│   └── products.json           # JSON file storing product information
│
├── static/                     # Static files directory
│   ├── css/
│   │   ├── style.css           # Main CSS styles for the website
│   │   └── chatbot.css         # CSS styles for the chatbot feature
│   │
│   ├── js/
│   │   ├── main.js             # Main JavaScript functionality
│   │   └── chatbot.js          # JavaScript for chatbot functionality
│   │
│   └── uploads/                # Directory for storing product images
│       └── .gitkeep            # Empty file to ensure directory is tracked in git
│
├── templates/                  # HTML templates directory
│   ├── base.html               # Base template with common layout elements
│   ├── index.html              # Homepage with product listing
│   ├── product_detail.html     # Product details page
│   ├── cart.html               # Shopping cart page
│   ├── checkout.html           # Checkout page
│   ├── about.html              # About Us page
│   ├── contact.html            # Contact Us page
│   │
│   └── admin/                  # Admin templates directory
│       ├── index.html          # Admin dashboard
│       ├── add_product.html    # Form for adding new products
│       └── edit_product.html   # Form for editing existing products
│
└── instance/                   # Instance-specific data
    └── database.db             # SQLite database (created at runtime)
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Storage**: JSON files
- **Interactive Features**: AJAX, Fetch API
- **Animations**: Animate.css
- **Icons**: Font Awesome 5

## Performance Optimization

The application includes several performance optimizations:

1. **Static Asset Caching**: CSS and JavaScript files are cached with appropriate headers
2. **Lazy Loading**: Images are lazy-loaded to improve initial page load time
3. **Minified Resources**: Production deployment should use minified CSS and JS
4. **Responsive Images**: Images are optimized for different screen sizes

## Browser Compatibility

The application is tested and compatible with:
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest version)
- Mobile browsers (iOS Safari, Android Chrome)

## Development Workflow

To contribute to this project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Testing

To run tests:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run tests
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support and Contact

For support or inquiries, please contact:
- Technical Support: support@crispychips.com
- Development Team: dev@crispychips.com

## Acknowledgements

- Bootstrap for the responsive design components
- Font Awesome for the icons
- Animate.css for animations
- Unsplash for stock photography