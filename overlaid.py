import os
import nibabel as nib
import numpy as np
import cv2

# Directory paths
original_dir = "/Users/colehanan/Desktop/original_images"
white_only_dir = "/Users/colehanan/Desktop/Regions_Data"
output_directory = "/Users/colehanan/Desktop/overlay_output"

# Ensure output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


def overlay_images(original_img, white_img):
    original_data = original_img.get_fdata()
    white_data = white_img.get_fdata()

    # Convert white_data to binary mask if not already
    white_data = np.where(white_data > 0, 255, 0).astype(np.uint8)

    # Initialize an empty array for overlaid images
    overlaid_data = np.zeros_like(original_data)

    for i in range(original_data.shape[-1]):  # Loop through each slice
        original_slice = original_data[:, :, i]
        white_slice = white_data[:, :, i]

        # Ensure the mask is the same size as the original slice
        if original_slice.shape != white_slice.shape:
            white_slice = cv2.resize(white_slice, (original_slice.shape[1], original_slice.shape[0]),
                                     interpolation=cv2.INTER_AREA)

        # Normalize the original slice for better visualization
        normalized_original = cv2.normalize(original_slice, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Ensure both are in the same color space
        if len(normalized_original.shape) == 2:  # Original is grayscale
            normalized_original = cv2.cvtColor(normalized_original, cv2.COLOR_GRAY2BGR)
        if len(white_slice.shape) == 2:  # Mask is grayscale
            white_slice = cv2.cvtColor(white_slice, cv2.COLOR_GRAY2BGR)

        # Overlay using cv2.addWeighted
        overlaid_slice = cv2.addWeighted(normalized_original, 0.7, white_slice, 0.3, 0)
        overlaid_data[:, :, i] = cv2.cvtColor(overlaid_slice,
                                              cv2.COLOR_BGR2GRAY)  # Convert back to grayscale for saving

    return nib.Nifti1Image(overlaid_data, original_img.affine, original_img.header)

# Processing files
for white_filename in os.listdir(white_only_dir):
    if white_filename.endswith(".nii.gz"):
        parts = white_filename.split('_')
        base_name = parts[0] + '_' + parts[1]
        original_filename = base_name + '.gz'
        original_file_path = os.path.join(original_dir, original_filename)
        white_file_path = os.path.join(white_only_dir, white_filename)

        print(f"Looking for original file: {original_filename}")

        if os.path.exists(original_file_path) and os.path.exists(white_file_path):
            # Load both images
            original_img = nib.load(original_file_path)
            white_img = nib.load(white_file_path)

            # Overlay images
            overlaid_img = overlay_images(original_img, white_img)

            # Save the overlaid image
            overlaid_filename = white_filename + '_overlaid.nii.gz'
            overlaid_file_path = os.path.join(output_directory, overlaid_filename)
            nib.save(overlaid_img, overlaid_file_path)
            print(f"Overlay saved: {overlaid_filename}")
        else:
            if not os.path.exists(original_file_path):
                print(f"Original file not found for {white_filename}")
            if not os.path.exists(white_file_path):
                print(f"White-only file not found for {white_filename}")

print("All possible overlays processed.")

