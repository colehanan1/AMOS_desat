import nibabel as nib

# Load the NIfTI file
nii = nib.load('/Users/colehanan/Desktop/processed_images3/amos_0054_region_12_masked.nii.gz')

# Get header information
header = nii.header

# Extract voxel dimensions (in mm)
voxel_dims = header.get_zooms()

# Print voxel dimensions
print("Voxel Dimensions:", voxel_dims)

# Extract the affine transformation matrix
affine = nii.affine
print("Affine Transformation Matrix:\n", affine)

# Access the image data
data = nii.get_fdata()
print("Data shape:", data.shape)

def mm_to_pixels(mm, voxel_size_mm):
    return mm / voxel_size_mm

# Example conversions
voxel_size_xy = 0.5703125  # Voxel size in mm for X and Y directions
distance_mm = 10  # Example distance in mm

pixels_xy = mm_to_pixels(distance_mm, voxel_size_xy)
print(f"{distance_mm} mm is approximately {pixels_xy:.2f} pixels on each of the X and Y axes.")
