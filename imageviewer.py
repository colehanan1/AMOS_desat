import napari
import nibabel as nib
import numpy as np

# Load the .nii.gz file
file_path = ("/Users/colehanan/Desktop/amos22/labelsTr/amos_0530.nii.gz")
img = nib.load(file_path)

# Convert the image data to a NumPy array
image_data = img.get_fdata()

# Launch the Napari viewer
viewer = napari.Viewer()

# Add the image to the Napari viewer
viewer.add_image(image_data, name='CT Scan', colormap='gray', contrast_limits=(np.min(image_data), np.max(image_data)))

nii_file = nib.load(file_path)

image_data = nii_file.get_fdata()

# Print basic information about the image
print(f"Dimensions: {nii_file.shape}")
print(f"Voxel spacing: {nii_file.header.get_zooms()}")

# Run Napari
napari.run()
