from PIL import Image, ImageDraw, ImageFont

def generate_text_image(text, font_path, image_size=(200, 100), bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    # Create a blank image with the specified background color
    image = Image.new('RGB', image_size, bg_color)
    draw = ImageDraw.Draw(image)

    # Load the font and calculate the text size
    font = ImageFont.truetype(font_path, 20)

    # Handle different versions of Pillow
    try:
        text_size = draw.textsize(text, font=font)
    except AttributeError:
        # For newer versions of Pillow
        text_size = draw.textbbox((0, 0), text, font=font)[2:4]

    # Calculate the position to center the text
    text_x = (image_size[0] - text_size[0]) / 2
    text_y = (image_size[1] - text_size[1]) / 2

    # Draw the text on the image
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    return image

# Function to generate product placeholder images
def generate_product_image(product_name, output_path, image_size=(400, 300), bg_color=(240, 240, 240), text_color=(60, 60, 60)):
    """
    Generate a placeholder image for a product with its name displayed.

    Args:
        product_name: Name of the product to display on the image
        output_path: Path where the image will be saved
        image_size: Tuple of (width, height) for the image
        bg_color: Background color as RGB tuple
        text_color: Text color as RGB tuple

    Returns:
        Path to the saved image
    """
    # Create a blank image with the specified background color
    image = Image.new('RGB', image_size, bg_color)
    draw = ImageDraw.Draw(image)

    # Try to use a common font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    # Handle different versions of Pillow
    try:
        text_size = draw.textsize(product_name, font=font)
    except AttributeError:
        # For newer versions of Pillow
        text_size = draw.textbbox((0, 0), product_name, font=font)[2:4]

    # Calculate the position to center the text
    text_x = (image_size[0] - text_size[0]) / 2
    text_y = (image_size[1] - text_size[1]) / 2

    # Draw a decorative border
    border_width = 10
    draw.rectangle(
        [(border_width, border_width),
         (image_size[0] - border_width, image_size[1] - border_width)],
        outline=(200, 200, 200),
        width=2
    )

    # Draw the product name
    draw.text((text_x, text_y), product_name, font=font, fill=text_color)

    # Add a small "Crispy Chips" watermark
    watermark = "Crispy Chips"
    watermark_font = ImageFont.load_default()

    # Handle different versions of Pillow
    try:
        watermark_size = draw.textsize(watermark, font=watermark_font)
    except AttributeError:
        # For newer versions of Pillow
        watermark_size = draw.textbbox((0, 0), watermark, font=watermark_font)[2:4]

    watermark_x = image_size[0] - watermark_size[0] - 10
    watermark_y = image_size[1] - watermark_size[1] - 10
    draw.text((watermark_x, watermark_y), watermark, font=watermark_font, fill=(150, 150, 150))

    # Save the image
    image.save(output_path)
    return output_path

# Example usage
if __name__ == "__main__":
    text = "Crispy Chips"
    font_path = "arial.ttf"  # Ensure this font file is available in your environment

    try:
        # Try to generate a simple text image
        image = generate_text_image(text, font_path)
        image.save("text_image.png")
        print("Created text_image.png")

        # Generate a product placeholder image
        product_name = "Classic Salted Chips"
        output_path = "product_placeholder.png"
        generate_product_image(product_name, output_path)
        print(f"Created product placeholder image at {output_path}")
    except Exception as e:
        print(f"Error generating images: {e}")
        # Fallback to a very simple approach if there are font issues
        image = Image.new('RGB', (200, 100), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), text, fill=(0, 0, 0))
        image.save("simple_text_image.png")
        print("Created simple_text_image.png as fallback")
