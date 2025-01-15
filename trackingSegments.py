import nibabel as nib
import numpy as np
import os

# Directory containing the .nii.gz files
directory_path = "/Users/colehanan/Desktop/amos22/labelsTr"

# Function to process each file
def process_file(file_path):
    img = nib.load(file_path)

    # Convert the image data to a NumPy array
    image_data = img.get_fdata()

    # Unique regions (excluding the background if it's zero)
    unique_regions = np.unique(image_data)
    if 0 in unique_regions:
        unique_regions = unique_regions[1:]  # Remove background if zero is considered background

    # Process each unique region
    for region in unique_regions:
        # Create a mask for the current region
        mask = image_data == region

        # Create a new NIfTI image only containing the current region
        masked_image = np.where(mask, image_data, 0)
        new_img = nib.Nifti1Image(masked_image, img.affine, img.header)

        # Save the new NIfTI image
        new_file_path = os.path.splitext(file_path)[0] + f'_region_{int(region)}.nii.gz'
        nib.save(new_img, new_file_path)

# Loop through all files in the specified directory
for filename in os.listdir(directory_path):
    if filename.endswith(".nii.gz") and 'region' not in filename:
        full_path = os.path.join(directory_path, filename)
        process_file(full_path)
        print(f"Processed {filename}")

