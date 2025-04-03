from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json
import os
import uuid
import time
import functools
from datetime import datetime
from werkzeug.utils import secure_filename
from config import ADMIN_USERNAME, ADMIN_PASSWORD, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Data file path
DATA_FILE = 'data/products.json'

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize products data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_product_image_url(product):
    """
    Returns an appropriate image URL for a product.
    If the product has a custom image, it will use that.
    Otherwise, it will return a high-quality stock image based on the category.
    """
    # Check if the product has a custom image that's not default.jpg
    if product.get('image') and product['image'] != 'default.jpg':
        # Check if the image file exists
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product['image'])
        if os.path.exists(image_path):
            return url_for('static', filename='uploads/' + product['image'])

    # If we get here, either the image doesn't exist or it's default.jpg
    # Map categories to beautiful stock images of chips from Unsplash
    category_images = {
        'Regular': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
        'Flavored': 'https://images.unsplash.com/photo-1621607512214-68297480165e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
        'Spicy': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
        'Organic': 'https://images.unsplash.com/photo-1599492406302-6fa433cf7a3f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'
    }

    # Get image based on category, or use a default if category not found
    category = product.get('category', 'Regular')
    return category_images.get(category, 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80')

def get_products():
    try:
        with open(DATA_FILE, 'r') as f:
            products = json.load(f)

            # Add image_url to each product
            for product in products:
                # Ensure we're working with a dictionary that can be modified
                if isinstance(product, dict):
                    product['image_url'] = get_product_image_url(product)
                    print(f"Product: {product['name']}, Image: {product.get('image', 'None')}, URL: {product['image_url']}")

            return products
    except Exception as e:
        print(f"Error loading products: {e}")
        return []

def save_products(products):
    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=4)

# Initialize shopping cart in session
@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = {}

# Home page - Product listing
@app.route('/')
def index():
    products = get_products()
    return render_template('index.html', products=products)

# About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Us page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Chatbot API endpoint
@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    data = request.json
    user_message = data.get('message', '')

    # Simple response logic - in a real app, you might use NLP or a more sophisticated system
    response = {
        'message': 'Thank you for your message. Our team will get back to you soon.',
        'timestamp': datetime.now().strftime('%H:%M %p')
    }

    # Add a delay to simulate processing
    time.sleep(1)

    return jsonify(response)

# Product detail page
@app.route('/product/<product_id>')
def product_detail(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    flash('Product not found', 'error')
    return redirect(url_for('index'))

# Add to cart
@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('index'))
    
    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    session['cart'] = cart
    flash(f'Added {quantity} {product["name"]} to your cart', 'success')
    return redirect(url_for('index'))

# View cart
@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    products = get_products()
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# Update cart
@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0))
    
    if quantity > 0:
        cart[product_id] = quantity
    else:
        if product_id in cart:
            del cart[product_id]
    
    session['cart'] = cart
    flash('Cart updated', 'success')
    return redirect(url_for('view_cart'))

# Remove from cart
@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        flash('Item removed from cart', 'success')
    return redirect(url_for('view_cart'))

# Checkout page
@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'error')
        return redirect(url_for('index'))
    
    products = get_products()
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

# Process order
@app.route('/place_order', methods=['POST'])
def place_order():
    # In a real application, you would process payment and save order details
    session['cart'] = {}
    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('index'))

# Login required decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return view(**kwargs)
    return wrapped_view

# Admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('You have been logged in successfully', 'success')
            return redirect(url_for('admin_index'))
        else:
            error = 'Invalid username or password'

    return render_template('admin/login.html', error=error)

# Admin logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('admin_login'))

# Admin routes
@app.route('/admin')
@login_required
def admin_index():
    products = get_products()
    return render_template('admin/index.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        category = request.form.get('category')
        
        if not name or price <= 0:
            flash('Please provide a valid name and price', 'error')
            return redirect(url_for('add_product'))
        
        # Handle image upload
        image = 'default.jpg'  # Default image
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add unique identifier to prevent filename collisions
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                image = unique_filename
        
        # Create new product
        new_product = {
            'id': str(uuid.uuid4()),
            'name': name,
            'description': description,
            'price': price,
            'image': image,
            'category': category
        }
        
        products = get_products()
        products.append(new_product)
        save_products(products)
        
        flash('Product added successfully', 'success')
        return redirect(url_for('admin_index'))
    
    return render_template('admin/add_product.html')

@app.route('/admin/edit/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('admin_index'))
    
    if request.method == 'POST':
        product['name'] = request.form.get('name')
        product['description'] = request.form.get('description')
        product['price'] = float(request.form.get('price', 0))
        product['category'] = request.form.get('category')
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add unique identifier to prevent filename collisions
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                
                # Remove old image if it's not the default
                if product['image'] != 'default.jpg':
                    try:
                        old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], product['image'])
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    except:
                        pass
                
                product['image'] = unique_filename
        
        save_products(products)
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin_index'))
    
    return render_template('admin/edit_product.html', product=product)

@app.route('/admin/delete/<product_id>')
@login_required
def delete_product(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product:
        # Remove product image if it's not the default
        if product['image'] != 'default.jpg':
            try:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], product['image'])
                if os.path.exists(image_path):
                    os.remove(image_path)
            except:
                pass
        
        # Remove product from list
        products = [p for p in products if p['id'] != product_id]
        save_products(products)
        flash('Product deleted successfully', 'success')
    else:
        flash('Product not found', 'error')
    
    return redirect(url_for('admin_index'))

if __name__ == '__main__':
    app.run(debug=True)