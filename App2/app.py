from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'fooddelivery_secret_key_2024'

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Data files paths
RESTAURANTS_FILE = 'data/restaurants.json'
MENU_ITEMS_FILE = 'data/menu_items.json'
USERS_FILE = 'data/users.json'
ORDERS_FILE = 'data/orders.json'

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize data files if they don't exist
def initialize_data_files():
    # Initialize restaurants data
    if not os.path.exists(RESTAURANTS_FILE):
        with open(RESTAURANTS_FILE, 'w') as f:
            json.dump([], f)
    
    # Initialize menu items data
    if not os.path.exists(MENU_ITEMS_FILE):
        with open(MENU_ITEMS_FILE, 'w') as f:
            json.dump([], f)
    
    # Initialize users data
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
    
    # Initialize orders data
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'w') as f:
            json.dump([], f)

initialize_data_files()

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_restaurants():
    with open(RESTAURANTS_FILE, 'r') as f:
        return json.load(f)

def get_menu_items():
    with open(MENU_ITEMS_FILE, 'r') as f:
        return json.load(f)

def get_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def get_orders():
    with open(ORDERS_FILE, 'r') as f:
        return json.load(f)

def save_restaurants(restaurants):
    with open(RESTAURANTS_FILE, 'w') as f:
        json.dump(restaurants, f, indent=4)

def save_menu_items(menu_items):
    with open(MENU_ITEMS_FILE, 'w') as f:
        json.dump(menu_items, f, indent=4)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=4)

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def restaurant_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_restaurant'):
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Import functools for decorators
import functools

# Routes
@app.route('/')
def index():
    restaurants = get_restaurants()
    return render_template('index.html', restaurants=restaurants)

@app.route('/restaurant/<restaurant_id>')
def restaurant_detail(restaurant_id):
    restaurants = get_restaurants()
    menu_items = get_menu_items()
    
    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('index'))
    
    restaurant_menu = [item for item in menu_items if item['restaurant_id'] == restaurant_id]
    
    return render_template('restaurant_detail.html', restaurant=restaurant, menu_items=restaurant_menu)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    restaurants = get_restaurants()
    menu_items = get_menu_items()
    
    # Filter restaurants by name or cuisine
    filtered_restaurants = [r for r in restaurants if query.lower() in r['name'].lower() or 
                           any(query.lower() in cuisine.lower() for cuisine in r['cuisines'])]
    
    # Filter menu items by name
    filtered_menu_items = [m for m in menu_items if query.lower() in m['name'].lower()]
    
    # Get unique restaurants from filtered menu items
    menu_restaurants = []
    for item in filtered_menu_items:
        restaurant = next((r for r in restaurants if r['id'] == item['restaurant_id']), None)
        if restaurant and restaurant not in filtered_restaurants and restaurant not in menu_restaurants:
            menu_restaurants.append(restaurant)
    
    # Combine results
    all_restaurants = filtered_restaurants + menu_restaurants
    
    return render_template('search_results.html', restaurants=all_restaurants, query=query)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type', 'customer')
        
        if not all([name, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        users = get_users()
        
        # Check if email already exists
        if any(user['email'] == email for user in users):
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = {
            'id': str(uuid.uuid4()),
            'name': name,
            'email': email,
            'password': generate_password_hash(password),
            'is_admin': False,
            'is_restaurant': user_type == 'restaurant',
            'created_at': datetime.now().isoformat()
        }
        
        users.append(new_user)
        save_users(users)
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([email, password]):
            flash('Email and password are required', 'danger')
            return redirect(url_for('login'))
        
        users = get_users()
        user = next((u for u in users if u['email'] == email), None)
        
        if not user or not check_password_hash(user['password'], password):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        
        # Set session variables
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['is_admin'] = user['is_admin']
        session['is_restaurant'] = user['is_restaurant']
        
        flash(f'Welcome back, {user["name"]}!', 'success')
        
        if user['is_admin']:
            return redirect(url_for('admin_dashboard'))
        elif user['is_restaurant']:
            return redirect(url_for('restaurant_dashboard'))
        else:
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []
    
    cart_items = session['cart']
    menu_items = get_menu_items()
    restaurants = get_restaurants()
    
    # Enrich cart items with menu item details
    enriched_cart = []
    total = 0
    
    for cart_item in cart_items:
        menu_item = next((item for item in menu_items if item['id'] == cart_item['item_id']), None)
        if menu_item:
            restaurant = next((r for r in restaurants if r['id'] == menu_item['restaurant_id']), None)
            
            item_total = cart_item['quantity'] * menu_item['price']
            total += item_total
            
            enriched_cart.append({
                'item_id': cart_item['item_id'],
                'name': menu_item['name'],
                'price': menu_item['price'],
                'quantity': cart_item['quantity'],
                'item_total': item_total,
                'restaurant_name': restaurant['name'] if restaurant else 'Unknown Restaurant'
            })
    
    return render_template('cart.html', cart_items=enriched_cart, total=total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 1))
    
    if not item_id:
        flash('Invalid item', 'danger')
        return redirect(url_for('index'))
    
    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    
    # Check if item already in cart
    cart = session['cart']
    item_in_cart = next((item for item in cart if item['item_id'] == item_id), None)
    
    if item_in_cart:
        item_in_cart['quantity'] += quantity
    else:
        cart.append({'item_id': item_id, 'quantity': quantity})
    
    session['cart'] = cart
    flash('Item added to cart', 'success')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 0))
    
    if not item_id:
        flash('Invalid item', 'danger')
        return redirect(url_for('cart'))
    
    cart = session.get('cart', [])
    
    if quantity <= 0:
        # Remove item from cart
        cart = [item for item in cart if item['item_id'] != item_id]
    else:
        # Update quantity
        item = next((item for item in cart if item['item_id'] == item_id), None)
        if item:
            item['quantity'] = quantity
    
    session['cart'] = cart
    flash('Cart updated', 'success')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        address = request.form.get('address')
        phone = request.form.get('phone')
        payment_method = request.form.get('payment_method')
        
        if not all([address, phone, payment_method]):
            flash('All fields are required', 'danger')
            return redirect(url_for('checkout'))
        
        # Create order
        cart_items = session['cart']
        menu_items = get_menu_items()
        
        order_items = []
        total = 0
        
        for cart_item in cart_items:
            menu_item = next((item for item in menu_items if item['id'] == cart_item['item_id']), None)
            if menu_item:
                item_total = cart_item['quantity'] * menu_item['price']
                total += item_total
                
                order_items.append({
                    'item_id': cart_item['item_id'],
                    'name': menu_item['name'],
                    'price': menu_item['price'],
                    'quantity': cart_item['quantity'],
                    'item_total': item_total,
                    'restaurant_id': menu_item['restaurant_id']
                })
        
        # Group items by restaurant
        restaurant_orders = {}
        for item in order_items:
            if item['restaurant_id'] not in restaurant_orders:
                restaurant_orders[item['restaurant_id']] = []
            restaurant_orders[item['restaurant_id']].append(item)
        
        # Create separate orders for each restaurant
        orders = get_orders()
        
        for restaurant_id, items in restaurant_orders.items():
            restaurant_total = sum(item['item_total'] for item in items)
            
            new_order = {
                'id': str(uuid.uuid4()),
                'user_id': session['user_id'],
                'restaurant_id': restaurant_id,
                'items': items,
                'total': restaurant_total,
                'address': address,
                'phone': phone,
                'payment_method': payment_method,
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            }
            
            orders.append(new_order)
        
        save_orders(orders)
        
        # Clear cart
        session['cart'] = []
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('orders'))
    
    # GET request - show checkout form
    cart_items = session['cart']
    menu_items = get_menu_items()
    restaurants = get_restaurants()
    
    # Enrich cart items with menu item details
    enriched_cart = []
    total = 0
    
    for cart_item in cart_items:
        menu_item = next((item for item in menu_items if item['id'] == cart_item['item_id']), None)
        if menu_item:
            restaurant = next((r for r in restaurants if r['id'] == menu_item['restaurant_id']), None)
            
            item_total = cart_item['quantity'] * menu_item['price']
            total += item_total
            
            enriched_cart.append({
                'item_id': cart_item['item_id'],
                'name': menu_item['name'],
                'price': menu_item['price'],
                'quantity': cart_item['quantity'],
                'item_total': item_total,
                'restaurant_name': restaurant['name'] if restaurant else 'Unknown Restaurant'
            })
    
    return render_template('checkout.html', cart_items=enriched_cart, total=total)

@app.route('/orders')
@login_required
def orders():
    all_orders = get_orders()
    restaurants = get_restaurants()
    
    # Filter orders for current user
    user_orders = [order for order in all_orders if order['user_id'] == session['user_id']]
    
    # Enrich orders with restaurant details
    for order in user_orders:
        restaurant = next((r for r in restaurants if r['id'] == order['restaurant_id']), None)
        order['restaurant_name'] = restaurant['name'] if restaurant else 'Unknown Restaurant'
    
    # Sort orders by creation date (newest first)
    user_orders.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('orders.html', orders=user_orders)

@app.route('/order/<order_id>')
@login_required
def order_detail(order_id):
    all_orders = get_orders()
    restaurants = get_restaurants()
    
    order = next((o for o in all_orders if o['id'] == order_id), None)
    
    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('orders'))
    
    # Check if user has permission to view this order
    if order['user_id'] != session['user_id'] and not session.get('is_admin') and not (session.get('is_restaurant') and order['restaurant_id'] == session.get('restaurant_id')):
        flash('You do not have permission to view this order', 'danger')
        return redirect(url_for('orders'))
    
    # Get restaurant details
    restaurant = next((r for r in restaurants if r['id'] == order['restaurant_id']), None)
    order['restaurant_name'] = restaurant['name'] if restaurant else 'Unknown Restaurant'
    
    return render_template('order_detail.html', order=order)

# Restaurant owner routes
@app.route('/restaurant/dashboard')
@login_required
@restaurant_required
def restaurant_dashboard():
    users = get_users()
    restaurants = get_restaurants()
    
    # Get current user
    user = next((u for u in users if u['id'] == session['user_id']), None)
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == user['id']), None)
    
    if not restaurant:
        # User is registered as restaurant but hasn't created a restaurant profile
        return redirect(url_for('restaurant_create'))
    
    # Get orders for this restaurant
    all_orders = get_orders()
    restaurant_orders = [order for order in all_orders if order['restaurant_id'] == restaurant['id']]
    
    # Sort orders by creation date (newest first)
    restaurant_orders.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Get menu items for this restaurant
    menu_items = get_menu_items()
    restaurant_menu = [item for item in menu_items if item['restaurant_id'] == restaurant['id']]
    
    return render_template('restaurant/dashboard.html', 
                          restaurant=restaurant, 
                          orders=restaurant_orders, 
                          menu_items=restaurant_menu)

@app.route('/restaurant/create', methods=['GET', 'POST'])
@login_required
@restaurant_required
def restaurant_create():
    users = get_users()
    restaurants = get_restaurants()
    
    # Check if user already has a restaurant
    user = next((u for u in users if u['id'] == session['user_id']), None)
    existing_restaurant = next((r for r in restaurants if r['owner_id'] == user['id']), None)
    
    if existing_restaurant:
        flash('You already have a restaurant', 'warning')
        return redirect(url_for('restaurant_dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        address = request.form.get('address')
        phone = request.form.get('phone')
        cuisines = request.form.getlist('cuisines')
        delivery_fee = float(request.form.get('delivery_fee', 0))
        min_order = float(request.form.get('min_order', 0))
        
        if not all([name, description, address, phone, cuisines]):
            flash('All fields are required', 'danger')
            return redirect(url_for('restaurant_create'))
        
        # Handle image upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid duplicates
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = f"uploads/{filename}"
        
        # Create new restaurant
        new_restaurant = {
            'id': str(uuid.uuid4()),
            'owner_id': session['user_id'],
            'name': name,
            'description': description,
            'address': address,
            'phone': phone,
            'cuisines': cuisines,
            'image': image,
            'delivery_fee': delivery_fee,
            'min_order': min_order,
            'rating': 0,
            'review_count': 0,
            'created_at': datetime.now().isoformat()
        }
        
        restaurants.append(new_restaurant)
        save_restaurants(restaurants)
        
        flash('Restaurant created successfully!', 'success')
        return redirect(url_for('restaurant_dashboard'))
    
    return render_template('restaurant/create.html')

@app.route('/restaurant/edit', methods=['GET', 'POST'])
@login_required
@restaurant_required
def restaurant_edit():
    restaurants = get_restaurants()
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == session['user_id']), None)
    
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('restaurant_dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        address = request.form.get('address')
        phone = request.form.get('phone')
        cuisines = request.form.getlist('cuisines')
        delivery_fee = float(request.form.get('delivery_fee', 0))
        min_order = float(request.form.get('min_order', 0))
        
        if not all([name, description, address, phone, cuisines]):
            flash('All fields are required', 'danger')
            return redirect(url_for('restaurant_edit'))
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid duplicates
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                restaurant['image'] = f"uploads/{filename}"
        
        # Update restaurant
        restaurant['name'] = name
        restaurant['description'] = description
        restaurant['address'] = address
        restaurant['phone'] = phone
        restaurant['cuisines'] = cuisines
        restaurant['delivery_fee'] = delivery_fee
        restaurant['min_order'] = min_order
        
        save_restaurants(restaurants)
        
        flash('Restaurant updated successfully!', 'success')
        return redirect(url_for('restaurant_dashboard'))
    
    return render_template('restaurant/edit.html', restaurant=restaurant)

@app.route('/restaurant/menu')
@login_required
@restaurant_required
def restaurant_menu():
    restaurants = get_restaurants()
    menu_items = get_menu_items()
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == session['user_id']), None)
    
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('restaurant_dashboard'))
    
    # Get menu items for this restaurant
    restaurant_menu = [item for item in menu_items if item['restaurant_id'] == restaurant['id']]
    
    # Group menu items by category
    menu_by_category = {}
    for item in restaurant_menu:
        category = item.get('category', 'Uncategorized')
        if category not in menu_by_category:
            menu_by_category[category] = []
        menu_by_category[category].append(item)
    
    return render_template('restaurant/menu.html', 
                          restaurant=restaurant, 
                          menu_by_category=menu_by_category)

@app.route('/restaurant/menu/add', methods=['GET', 'POST'])
@login_required
@restaurant_required
def add_menu_item():
    restaurants = get_restaurants()
    menu_items = get_menu_items()
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == session['user_id']), None)
    
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('restaurant_dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        category = request.form.get('category')
        is_veg = request.form.get('is_veg') == 'on'
        is_available = request.form.get('is_available') == 'on'
        
        if not all([name, description, price, category]):
            flash('All fields are required', 'danger')
            return redirect(url_for('add_menu_item'))
        
        # Handle image upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid duplicates
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = f"uploads/{filename}"
        
        # Create new menu item
        new_item = {
            'id': str(uuid.uuid4()),
            'restaurant_id': restaurant['id'],
            'name': name,
            'description': description,
            'price': price,
            'category': category,
            'image': image,
            'is_veg': is_veg,
            'is_available': is_available,
            'created_at': datetime.now().isoformat()
        }
        
        menu_items.append(new_item)
        save_menu_items(menu_items)
        
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('restaurant_menu'))
    
    return render_template('restaurant/add_menu_item.html', restaurant=restaurant)

@app.route('/restaurant/menu/edit/<item_id>', methods=['GET', 'POST'])
@login_required
@restaurant_required
def edit_menu_item(item_id):
    restaurants = get_restaurants()
    menu_items = get_menu_items()
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == session['user_id']), None)
    
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('restaurant_dashboard'))
    
    # Get menu item
    menu_item = next((item for item in menu_items if item['id'] == item_id), None)
    
    if not menu_item:
        flash('Menu item not found', 'danger')
        return redirect(url_for('restaurant_menu'))
    
    # Check if menu item belongs to this restaurant
    if menu_item['restaurant_id'] != restaurant['id']:
        flash('You do not have permission to edit this menu item', 'danger')
        return redirect(url_for('restaurant_menu'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        category = request.form.get('category')
        is_veg = request.form.get('is_veg') == 'on'
        is_available = request.form.get('is_available') == 'on'
        
        if not all([name, description, price, category]):
            flash('All fields are required', 'danger')
            return redirect(url_for('edit_menu_item', item_id=item_id))
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid duplicates
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                menu_item['image'] = f"uploads/{filename}"
        
        # Update menu item
        menu_item['name'] = name
        menu_item['description'] = description
        menu_item['price'] = price
        menu_item['category'] = category
        menu_item['is_veg'] = is_veg
        menu_item['is_available'] = is_available
        
        save_menu_items(menu_items)
        
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('restaurant_menu'))
    
    return render_template('restaurant/edit_menu_item.html', restaurant=restaurant, menu_item=menu_item)

@app.route('/restaurant/menu/delete/<item_id>', methods=['POST'])
@login_required
@restaurant_required
def delete_menu_item(item_id):
    restaurants = get_restaurants()
    menu_items = get_menu_items()
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == session['user_id']), None)
    
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('restaurant_dashboard'))
    
    # Get menu item
    menu_item = next((item for item in menu_items if item['id'] == item_id), None)
    
    if not menu_item:
        flash('Menu item not found', 'danger')
        return redirect(url_for('restaurant_menu'))
    
    # Check if menu item belongs to this restaurant
    if menu_item['restaurant_id'] != restaurant['id']:
        flash('You do not have permission to delete this menu item', 'danger')
        return redirect(url_for('restaurant_menu'))
    
    # Delete menu item
    menu_items = [item for item in menu_items if item['id'] != item_id]
    save_menu_items(menu_items)
    
    flash('Menu item deleted successfully!', 'success')
    return redirect(url_for('restaurant_menu'))

@app.route('/restaurant/orders')
@login_required
@restaurant_required
def restaurant_orders():
    restaurants = get_restaurants()
    all_orders = get_orders()
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == session['user_id']), None)
    
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('restaurant_dashboard'))
    
    # Get orders for this restaurant
    restaurant_orders = [order for order in all_orders if order['restaurant_id'] == restaurant['id']]
    
    # Sort orders by creation date (newest first)
    restaurant_orders.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('restaurant/orders.html', restaurant=restaurant, orders=restaurant_orders)

@app.route('/restaurant/order/<order_id>')
@login_required
@restaurant_required
def restaurant_order_detail(order_id):
    restaurants = get_restaurants()
    all_orders = get_orders()
    users = get_users()
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == session['user_id']), None)
    
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('restaurant_dashboard'))
    
    # Get order
    order = next((o for o in all_orders if o['id'] == order_id), None)
    
    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('restaurant_orders'))
    
    # Check if order belongs to this restaurant
    if order['restaurant_id'] != restaurant['id']:
        flash('You do not have permission to view this order', 'danger')
        return redirect(url_for('restaurant_orders'))
    
    # Get customer details
    customer = next((u for u in users if u['id'] == order['user_id']), None)
    
    return render_template('restaurant/order_detail.html', 
                          restaurant=restaurant, 
                          order=order, 
                          customer=customer)

@app.route('/restaurant/order/<order_id>/update', methods=['POST'])
@login_required
@restaurant_required
def update_order_status(order_id):
    restaurants = get_restaurants()
    all_orders = get_orders()
    
    # Get restaurant owned by user
    restaurant = next((r for r in restaurants if r['owner_id'] == session['user_id']), None)
    
    if not restaurant:
        flash('Restaurant not found', 'danger')
        return redirect(url_for('restaurant_dashboard'))
    
    # Get order
    order = next((o for o in all_orders if o['id'] == order_id), None)
    
    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('restaurant_orders'))
    
    # Check if order belongs to this restaurant
    if order['restaurant_id'] != restaurant['id']:
        flash('You do not have permission to update this order', 'danger')
        return redirect(url_for('restaurant_orders'))
    
    # Update order status
    status = request.form.get('status')
    if status in ['pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled']:
        order['status'] = status
        save_orders(all_orders)
        flash('Order status updated successfully!', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('restaurant_order_detail', order_id=order_id))

# Admin routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    users = get_users()
    restaurants = get_restaurants()
    all_orders = get_orders()
    
    # Count statistics
    user_count = len([u for u in users if not u['is_admin'] and not u['is_restaurant']])
    restaurant_count = len(restaurants)
    order_count = len(all_orders)
    
    # Calculate total revenue
    total_revenue = sum(order['total'] for order in all_orders if order['status'] == 'delivered')
    
    # Get recent orders
    recent_orders = sorted(all_orders, key=lambda x: x['created_at'], reverse=True)[:10]
    
    # Enrich orders with restaurant details
    for order in recent_orders:
        restaurant = next((r for r in restaurants if r['id'] == order['restaurant_id']), None)
        order['restaurant_name'] = restaurant['name'] if restaurant else 'Unknown Restaurant'
    
    return render_template('admin/dashboard.html', 
                          user_count=user_count,
                          restaurant_count=restaurant_count,
                          order_count=order_count,
                          total_revenue=total_revenue,
                          recent_orders=recent_orders)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = get_users()
    
    # Sort users by creation date (newest first)
    users.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('admin/users.html', users=users)

@app.route('/admin/restaurants')
@login_required
@admin_required
def admin_restaurants():
    restaurants = get_restaurants()
    users = get_users()
    
    # Enrich restaurants with owner details
    for restaurant in restaurants:
        owner = next((u for u in users if u['id'] == restaurant['owner_id']), None)
        restaurant['owner_name'] = owner['name'] if owner else 'Unknown Owner'
    
    # Sort restaurants by creation date (newest first)
    restaurants.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('admin/restaurants.html', restaurants=restaurants)

@app.route('/admin/orders')
@login_required
@admin_required
def admin_orders():
    all_orders = get_orders()
    restaurants = get_restaurants()
    users = get_users()
    
    # Enrich orders with restaurant and user details
    for order in all_orders:
        restaurant = next((r for r in restaurants if r['id'] == order['restaurant_id']), None)
        user = next((u for u in users if u['id'] == order['user_id']), None)
        
        order['restaurant_name'] = restaurant['name'] if restaurant else 'Unknown Restaurant'
        order['user_name'] = user['name'] if user else 'Unknown User'
    
    # Sort orders by creation date (newest first)
    all_orders.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('admin/orders.html', orders=all_orders)

@app.route('/admin/order/<order_id>')
@login_required
@admin_required
def admin_order_detail(order_id):
    all_orders = get_orders()
    restaurants = get_restaurants()
    users = get_users()
    
    # Get order
    order = next((o for o in all_orders if o['id'] == order_id), None)
    
    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('admin_orders'))
    
    # Get restaurant and customer details
    restaurant = next((r for r in restaurants if r['id'] == order['restaurant_id']), None)
    customer = next((u for u in users if u['id'] == order['user_id']), None)
    
    return render_template('admin/order_detail.html', 
                          order=order, 
                          restaurant=restaurant, 
                          customer=customer)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)