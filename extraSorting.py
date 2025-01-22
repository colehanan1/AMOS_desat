import os
import re
from shutil import move

def sort_files_into_regions(base_path):
    # Ensure the base_path exists and is a directory
    if not os.path.isdir(base_path):
        print(f"The path {base_path} does not exist or is not a directory.")
        return

    # Create the region directories if they do not exist
    for i in range(1, 13):
        region_dir = os.path.join(base_path, f'region_{i}')
        if not os.path.exists(region_dir):
            os.mkdir(region_dir)
            print(f"Created directory: {region_dir}")

    # Pattern to match files that should be moved
    pattern = re.compile(r'region_(\d+)')

    # Move files to their respective region directories
    for file_name in os.listdir(base_path):
        match = pattern.search(file_name)
        if match:
            region_number = match.group(1)
            if 1 <= int(region_number) <= 12:  # Ensure it's a valid region number
                file_path = os.path.join(base_path, file_name)
                target_dir = os.path.join(base_path, f'region_{region_number}')
                move(file_path, target_dir)
                print(f"Moved {file_name} to {target_dir}")

def main():
    base_path = '/Users/colehanan/Desktop/slicedUpImage4'
    sort_files_into_regions(base_path)

if __name__ == "__main__":
    main()
