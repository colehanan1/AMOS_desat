import os
import nibabel as nib
import numpy as np

# Directory paths
original_dir = "/Users/colehanan/Desktop/original_images"
white_only_dir = "/Users/colehanan/Desktop/Regions_Data_MRI"
output_directory = "/Users/colehanan/Desktop/processed_images1"

# Ensure output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def apply_mask(original_img, mask_img):
    mask_data = mask_img.get_fdata()
    binary_mask = np.where(mask_data > 0, 1, 0)

    original_data = original_img.get_fdata()
    masked_data = np.zeros_like(original_data)
    masked_data[binary_mask == 1] = original_data[binary_mask == 1]

    # Ensure the background is explicitly black
    masked_data[binary_mask == 0] = 0
    return nib.Nifti1Image(masked_data, original_img.affine, original_img.header)

def process_files():
    for white_filename in os.listdir(white_only_dir):
        if white_filename.endswith("nii.gz"):
            parts = white_filename.split('_')
            base_name = '_'.join(parts[:2])

            original_filename = base_name + '.gz'
            original_file_path = os.path.join(original_dir, original_filename)
            white_file_path = os.path.join(white_only_dir, white_filename)

            print(f"Looking for original file: {original_filename}")

            if os.path.exists(original_file_path) and os.path.exists(white_file_path):
                original_img = nib.load(original_file_path)
                white_img = nib.load(white_file_path)

                masked_img = apply_mask(original_img, white_img)

                masked_filename = white_filename.replace('.nii.gz', '_.nii.gz')
                masked_file_path = os.path.join(output_directory, masked_filename)
                nib.save(masked_img, masked_file_path)
                print(f"Masked image saved: {masked_file_path}")
            else:
                if not os.path.exists(original_file_path):
                    print(f"Original file not found for {white_filename}")
                if not os.path.exists(white_file_path):
                    print(f"White-only file not found for {white_filename}")

process_files()
print("All possible masks processed.")
