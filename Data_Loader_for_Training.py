import torch
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import os
import numpy as np


class SliceDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.slice_files = []
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.tif') or file.endswith('.tiff'):
                    self.slice_files.append(os.path.join(subdir, file))

        print(f"Initialized dataset with {len(self.slice_files)} images.")

    def __len__(self):
        return len(self.slice_files)

    def __getitem__(self, idx):
        slice_file = self.slice_files[idx]
        with Image.open(slice_file) as img:
            # Convert the image to grayscale (if it's not already)
            img = img.convert('L')
            slice_data = np.array(img)
            print(f"Loaded image {slice_file} with shape {slice_data.shape} and dtype {slice_data.dtype}")

        if self.transform:
            slice_data = self.transform(slice_data)
            print(f"Transformed image {slice_file}")

        return slice_data


# Define transformations, including resizing all images to 256x256
transformations = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((256, 256)),  # Resize all images to 256x256
    transforms.Normalize(mean=[0.5], std=[0.5])
])

# Create dataset and DataLoader
dataset = SliceDataset(root_dir='/Users/colehanan/Desktop/slicedUpImages', transform=transformations)
dataloader = DataLoader(dataset, batch_size=10, shuffle=True)

# Iterate through the DataLoader
if __name__ == "__main__":
    for i, data in enumerate(dataloader):
        print(f"Batch {i}: Data shape {data.shape}, Data type {data.dtype}")
        # Add a condition to break early for testing so that you don't process everything during debugging
        if i == 1:  # Limit to processing just two batches for debugging
            break
