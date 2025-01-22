import os

def rename_files_in_folder(folder_path, name_mapping):
    for file_name in os.listdir(folder_path):
        if file_name.startswith('amos_') and file_name.endswith('.png'):
            # Extract the relevant parts from the filename
            parts = file_name.split('_')
            amos_code = parts[1]  # The numeric code, e.g., '0025'

            # Check if this numeric code is in the mapping dictionary
            if amos_code in name_mapping:
                new_base_name = name_mapping[amos_code]  # Get the new base name, e.g., 'CT_1'
                slice_info = parts[-1]  # This should be 'slice_XXXX.tif'
                new_name = f"{new_base_name}_{slice_info}"  # Construct the new filename without region info
                old_file_path = os.path.join(folder_path, file_name)
                new_file_path = os.path.join(folder_path, new_name)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed {old_file_path} to {new_file_path}")
            else:
                print(f"No mapping found for: {amos_code}")
        else:
            print(f"Skipping file: {file_name}")

def main():
    output_base_folder = '/Users/colehanan/Desktop/slicedUpImage4'  # Update this path as necessary
    name_mapping = {
        '0001': 'CT_1',
        '0025': 'CT_2',
        '0054': 'CT_3',
        '0058': 'CT_4',
        '0508': 'MRI_1',
        '0510': 'MRI_2',
        '0551': 'MRI_3',
        '0557': 'MRI_4'
    }

    for region_folder in os.listdir(output_base_folder):
        folder_path = os.path.join(output_base_folder, region_folder)
        if os.path.isdir(folder_path):
            rename_files_in_folder(folder_path, name_mapping)

if __name__ == "__main__":
    main()
