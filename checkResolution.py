from PIL import Image
import os

def check_image_resolution(directory):
    # List all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            # Construct the full file path
            file_path = os.path.join(directory, filename)
            # Open the image file
            with Image.open(file_path) as img:
                # Get image size
                width, height = img.size
                print(f"The resolution of {filename} is {width}x{height} pixels.")

# Specify the directory containing the images
image_directory = ('/Users/colehanan/Desktop/finalCopy/group_8/CT_4')  # Modify this path to your actual directory

# Call the function
check_image_resolution(image_directory)
