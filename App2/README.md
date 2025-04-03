# FoodExpress - Food Delivery Web Application

A Flask-based food delivery web application similar to Zomato/Swiggy. This application allows users to browse restaurants, view menus, place orders, and track deliveries. It also includes restaurant owner and admin dashboards for managing the platform.

## Features

### Customer Features
- **Restaurant Browsing**: Browse through a variety of restaurants
- **Search & Filters**: Search for restaurants or dishes, filter by cuisine
- **Menu Viewing**: View detailed restaurant menus with item descriptions and prices
- **Cart Management**: Add items to cart, update quantities, and remove items
- **Checkout Process**: Simple checkout form for placing orders
- **Order Tracking**: Track the status of your orders
- **User Accounts**: Register, login, and manage your profile

### Restaurant Owner Features
- **Restaurant Management**: Create and manage restaurant profile
- **Menu Management**: Add, edit, and remove menu items
- **Order Management**: View and update order statuses
- **Analytics**: View basic sales and order statistics

### Admin Features
- **Platform Management**: Oversee all restaurants and users
- **Order Monitoring**: Monitor all orders across the platform
- **User Management**: Manage user accounts and permissions

## Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/food-express.git
   cd food-express
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

## Project Structure

```
food_express/
│
├── app.py                      # Main Flask application with all routes and logic
├── run.py                      # Script to run the application
├── requirements.txt            # List of Python dependencies
├── README.md                   # Project documentation
│
├── data/                       # Data storage directory
│   ├── restaurants.json        # JSON file storing restaurant information
│   ├── menu_items.json         # JSON file storing menu items
│   ├── users.json              # JSON file storing user accounts
│   └── orders.json             # JSON file storing orders
│
├── static/                     # Static files directory
│   ├── css/
│   │   └── style.css           # Main CSS styles for the website
│   │
│   ├── js/
│   │   └── main.js             # Main JavaScript functionality
│   │
│   └── uploads/                # Directory for storing uploaded images
│
└── templates/                  # HTML templates directory
    ├── base.html               # Base template with common layout elements
    ├── index.html              # Homepage with restaurant listing
    ├── restaurant_detail.html  # Restaurant details and menu page
    ├── search_results.html     # Search results page
    ├── cart.html               # Shopping cart page
    ├── checkout.html           # Checkout page
    ├── orders.html             # User orders page
    ├── login.html              # Login page
    ├── register.html           # Registration page
    │
    ├── restaurant/             # Restaurant owner templates
    │   ├── dashboard.html      # Restaurant owner dashboard
    │   ├── menu.html           # Menu management page
    │   ├── orders.html         # Restaurant orders page
    │   └── ...                 # Other restaurant management pages
    │
    └── admin/                  # Admin templates
        ├── dashboard.html      # Admin dashboard
        ├── restaurants.html    # Restaurant management page
        ├── users.html          # User management page
        └── ...                 # Other admin pages
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Storage**: JSON files (for simplicity)
- **Authentication**: Session-based authentication
- **Icons**: Font Awesome 5

## Default Admin Account

For testing purposes, a default admin account is created:
- Email: admin@fooddelivery.com
- Password: admin123

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the responsive design components
- Font Awesome for the icons
- Unsplash for stock photography