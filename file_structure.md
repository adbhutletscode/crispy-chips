# Crispy Chips Web Application - File Structure

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
│   │   └── style.css           # Custom CSS styles for the website
│   │
│   ├── js/
│   │   └── main.js             # JavaScript functionality
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
│   │
│   └── admin/                  # Admin templates directory
│       ├── index.html          # Admin dashboard
│       ├── add_product.html    # Form for adding new products
│       └── edit_product.html   # Form for editing existing products
│
└── text_to_image.py            # Utility script for generating text images
```

## Directory and File Descriptions

### Root Directory Files

- **app.py**: The main Flask application file containing all route definitions, view functions, and application logic.
- **run.py**: A simple script to run the Flask application.
- **requirements.txt**: Lists all Python package dependencies needed for the project.
- **README.md**: Documentation for the project, including setup instructions and features.
- **.gitignore**: Specifies files and directories that should be ignored by Git.
- **text_to_image.py**: A utility script for generating text images using PIL.

### Data Directory

- **data/products.json**: JSON file that stores all product information including IDs, names, descriptions, prices, images, and categories.

### Static Directory

- **static/css/style.css**: Contains all custom CSS styles for the website.
- **static/js/main.js**: Contains JavaScript code for interactive features.
- **static/uploads/**: Directory where uploaded product images are stored.

### Templates Directory

- **templates/base.html**: The base template that defines the common layout, navigation, and footer.
- **templates/index.html**: The homepage template showing the product catalog.
- **templates/product_detail.html**: Template for displaying detailed information about a specific product.
- **templates/cart.html**: Template for the shopping cart page.
- **templates/checkout.html**: Template for the checkout process.

### Admin Templates Directory

- **templates/admin/index.html**: Template for the admin dashboard showing all products.
- **templates/admin/add_product.html**: Form template for adding new products.
- **templates/admin/edit_product.html**: Form template for editing existing products.