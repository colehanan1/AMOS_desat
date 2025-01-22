import os
from shutil import move


def rename_folders(base_path, mappings):
    temp_mappings = {key: f"temp_{key}" for key in mappings.keys()}

    # Step 1: Rename all directories to temporary names
    for old_name, temp_name in temp_mappings.items():
        old_path = os.path.join(base_path, old_name)
        temp_path = os.path.join(base_path, temp_name)
        if os.path.exists(old_path):
            print(f"Renaming {old_name} to {temp_name}")
            move(old_path, temp_path)

    # Step 2: Rename from temporary names to final names
    for temp_name, final_name in [(temp_mappings[old], mappings[old]) for old in mappings]:
        temp_path = os.path.join(base_path, temp_name)
        final_path = os.path.join(base_path, final_name)
        if os.path.exists(temp_path):
            print(f"Renaming {temp_name} to {final_name}")
            move(temp_path, final_path)


def main():
    base_path = '/Users/colehanan/Desktop/slicedUpImage4'
    mappings = {
        'region_1': 'region_7',
        'region_2': 'region_4',
        'region_3': 'region_12',
        'region_4': 'region_9',
        'region_5': 'region_8',
        'region_6': 'region_2',
        'region_7': 'region_10',
        'region_8': 'region_3',
        'region_9': 'region_11',
        'region_10': 'region_5',
        'region_11': 'region_6',
        'region_12': 'region_1'
    }

    rename_folders(base_path, mappings)


if __name__ == "__main__":
    main()
