"""
Configuration file for Crispy Chips application.
This file contains sensitive information like admin credentials and should be kept secure.
In a production environment, these values should be stored as environment variables.
"""

# Admin credentials
ADMIN_USERNAME = "admin"
# In a real application, you would store a hashed password, not plaintext
ADMIN_PASSWORD = "crispy123"

# Secret key for session
SECRET_KEY = "crispy_chips_secret_key_change_in_production"