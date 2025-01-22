import os

def rename_folders_and_files(base_folder):
    # Iterate over each subfolder in the base folder
    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Check if it's a directory
            # Iterate over each nested folder inside the subfolder
            for nested_folder in os.listdir(subfolder_path):
                nested_folder_path = os.path.join(subfolder_path, nested_folder)
                if os.path.isdir(nested_folder_path):  # Ensure it's a directory
                    new_nested_folder_name = nested_folder.replace('amos_0599', 'MRI_3')
                    new_nested_folder_path = os.path.join(subfolder_path, new_nested_folder_name)
                    # Rename the nested folder if new name is different
                    if new_nested_folder_name != nested_folder:
                        os.rename(nested_folder_path, new_nested_folder_path)
                    else:
                        new_nested_folder_path = nested_folder_path

                    # Iterate over all files in the newly named nested folder
                    for filename in os.listdir(new_nested_folder_path):
                        if filename.endswith('.png'):
                            file_path = os.path.join(new_nested_folder_path, filename)
                            new_filename = filename.replace('amos_0599', 'MRI_3')
                            new_file_path = os.path.join(new_nested_folder_path, new_filename)
                            # Rename the file if new name is different
                            if new_filename != filename:
                                os.rename(file_path, new_file_path)

if __name__ == '__main__':
    base_folder = '/Users/colehanan/Desktop/slicedUpImage4'  # Update this to your actual base folder path
    rename_folders_and_files(base_folder)
