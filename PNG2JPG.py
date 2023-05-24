from PIL import Image
import os

def convert_jpg_to_png(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Resize the image
    max_size = (50, 50)  # Specify the maximum width and height for the resized image
    image.thumbnail(max_size)

    # Create a new file name for the PNG image
    png_image_path = os.path.splitext(image_path)[0] + '.png'

    # Convert and save the image as PNG
    image.save(png_image_path, 'PNG')

    # Close the image file
    image.close()

    print(f"Image converted and saved as: {png_image_path}")


# Specify the path to your JPG image
jpg_image_path = r'C:\Users\eulal\OneDrive - Universidad de Guanajuato\Escritorio\GUIPY\bird3.jpg'

# Call the function to convert the JPG image to PNG and resize it
convert_jpg_to_png(jpg_image_path)