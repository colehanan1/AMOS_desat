import os
import shutil

def organize_images(folder_path):
    # Create directories for CT and MRI types if they don't exist
    categories = ['CT_1', 'CT_2', 'CT_3', 'CT_4', 'MRI_1', 'MRI_2', 'MRI_3', 'MRI_4']
    for category in categories:
        category_path = os.path.join(folder_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            print(f"Created directory: {category_path}")

    # Move files into their respective directories
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.tif'):
            # Identify the category from the filename
            for category in categories:
                if file_name.startswith(category):
                    src_path = os.path.join(folder_path, file_name)
                    dst_path = os.path.join(folder_path, category, file_name)
                    shutil.move(src_path, dst_path)
                    print(f"Moved {file_name} to {dst_path}")
                    break

def main():
    output_base_folder = '/Users/colehanan/Desktop/slicedUpImage4'  # Update this path as necessary

    # Apply the organization to each subfolder
    for region_folder in os.listdir(output_base_folder):
        folder_path = os.path.join(output_base_folder, region_folder)
        if os.path.isdir(folder_path):
            organize_images(folder_path)
            print(f"Organized images in {folder_path}")

if __name__ == "__main__":
    main()
