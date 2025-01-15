import os
import nibabel as nib
import numpy as np

# Directory where the mask files are located
directory_path = "/Users/colehanan/Desktop/Regions_Data"

# Directory to save the new files
output_directory = "/Users/colehanan/Desktop/Regions_Data_Masks"

# Check and create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Process each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".nii.gz") and 'region' in filename:
        full_path = os.path.join(directory_path, filename)

        # Load the NIfTI file
        img = nib.load(full_path)
        image_data = img.get_fdata()

        # Create a new image array where all non-white (non-max value) pixels are set to 0
        max_value = np.max(image_data)
        white_regions_only = np.where(image_data == max_value, max_value, 0)

        # Create a new NIfTI image using the original affine and header for correct orientation and metadata
        new_img = nib.Nifti1Image(white_regions_only, img.affine, img.header)

        # Define the new filename
        new_filename = os.path.splitext(filename)[0] + '_white_only.nii.gz'
        new_file_path = os.path.join(output_directory, new_filename)

        # Save the new NIfTI file
        nib.save(new_img, new_file_path)
        print(f"Processed and saved: {new_filename}")

print("All files processed.")

