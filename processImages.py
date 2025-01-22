import os
import nibabel as nib
import numpy as np
import cv2
from imgaug import augmenters as iaa

# Directory paths
input_dir = "/Users/colehanan/Desktop/processed_images"  # Adjusted to where your overlaid NIfTI files are stored
output_dir = "/Users/colehanan/Desktop/processed_images_augmented"  # Output directory for augmented images

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Augmentation sequence
augment_seq = iaa.Sequential([
    iaa.Fliplr(0.5),  # horizontal flips
    iaa.Crop(percent=(0, 0.1)),  # random crops
    iaa.Affine(
        scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},  # scaling
        translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)},  # translation
        rotate=(-25, 25)  # rotation
    )
])

def normalize_data(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def process_files():
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.nii.gz'):
            file_path = os.path.join(input_dir, file_name)
            img = nib.load(file_path)
            data = img.get_fdata()
            normalized_data = normalize_data(data)

            # Process each slice for augmentation
            augmented_data = np.zeros_like(normalized_data)
            for i in range(normalized_data.shape[-1]):
                slice = normalized_data[..., i]
                slice_3c = cv2.cvtColor((slice * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)  # Convert to 3-channel
                augmented_slice = augment_seq(images=[slice_3c])[0]
                augmented_data[..., i] = cv2.cvtColor(augmented_slice,
                                                      cv2.COLOR_BGR2GRAY) / 255.0  # Back to grayscale and normalize

            # Save the processed data
            output_file_path = os.path.join(output_dir, file_name)
            nib.save(nib.Nifti1Image(augmented_data, img.affine, img.header), output_file_path)
            print(f"Processed and saved: {output_file_path}")

process_files()
print("Processing completed.")
