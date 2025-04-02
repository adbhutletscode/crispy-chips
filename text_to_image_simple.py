"""
Simplified version of text_to_image.py that doesn't require Pillow.
This is a placeholder that returns file paths without actually generating images.
"""

def generate_text_image(text, font_path, image_size=(200, 100), bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    """
    Placeholder function that would normally generate a text image.
    """
    print(f"[PLACEHOLDER] Would generate text image with text: {text}")
    return None

def generate_product_image(product_name, output_path, image_size=(400, 300), bg_color=(240, 240, 240), text_color=(60, 60, 60)):
    """
    Placeholder function that would normally generate a product image.
    Instead of generating an image, it just returns the output path.
    """
    print(f"[PLACEHOLDER] Would generate product image for: {product_name} at {output_path}")
    
    # Create an empty file at the output path
    with open(output_path, 'w') as f:
        f.write(f"Placeholder for {product_name} image")
    
    return output_path

# Example usage
if __name__ == "__main__":
    print("This is a simplified version of text_to_image.py that doesn't require Pillow.")
    print("It provides placeholder functions that don't actually generate images.")