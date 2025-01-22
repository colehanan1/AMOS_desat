import os
import nibabel as nib
import numpy as np
from PIL import Image

def slice_3d_image(image_path, output_base_folder):
    try:
        img = nib.load(image_path)
    except Exception as e:
        print(f"Failed to load {image_path}: {e}")
        return

    data = img.get_fdata()
    volume_min = np.min(data)
    volume_max = np.max(data)

    base_name = os.path.basename(image_path).split('.')[0]
    output_folder = os.path.join(output_base_folder, base_name)

    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            print(f"Failed to create directory {output_folder}: {e}")
            return

    slices = data.shape[2]
    for i in range(slices):
        slice_2d = data[:, :, i]

        if volume_max != volume_min:
            slice_normalized = (255 * (slice_2d - volume_min) / (volume_max - volume_min)).astype(np.uint8)
        else:
            slice_normalized = np.zeros_like(slice_2d, dtype=np.uint8)

        slice_output_path = os.path.join(output_folder, f'{base_name}_slice_{i:04d}.png')
        try:
            img = Image.fromarray(slice_normalized)
            img.save(slice_output_path)
        except Exception as e:
            print(f"Failed to save image {slice_output_path}: {e}")

def main(input_folder, output_base_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.nii.gz'):
            image_path = os.path.join(input_folder, file_name)
            slice_3d_image(image_path, output_base_folder)
            print(f"Sliced {image_path}")


if __name__ == '__main__':
    input_folder = '/Users/colehanan/Desktop/processed_images1'  # Update this path to your actual folder where files are stored
    output_base_folder = '/Users/colehanan/Desktop/slicedUpImage4'  # Update this to your desired output folder
    main(input_folder, output_base_folder)
