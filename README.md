# AMOS Dataset Image Utilities

This repository collects standalone Python utilities for preparing AMOS medical imaging data (NIfTI volumes and derived 2D slices). The scripts focus on isolating organ regions, overlaying masks on original scans, slicing volumes into PNG files, organizing the outputs, and loading the resulting images for model training.

## Repository overview
- **Data preparation workflow**: Segment NIfTI label volumes into per-region masks, filter masks to isolate the brightest region, apply those masks to original CT/MRI scans, and overlay the masks for visualization.
- **Slicing and organization**: Convert the masked 3D volumes into normalized 2D PNG slices and sort them into consistent region and modality folders before renaming to modality-aware filenames.
- **Augmentation and loading**: Augment overlaid volumes slice-by-slice and load normalized 2D slices into PyTorch DataLoaders for downstream training.

## Script reference
Each script is self-contained; update the hard-coded file system paths to match your environment before running.

- `trackingSegments.py`: Splits each labeled NIfTI volume into separate per-region mask files by extracting unique nonzero labels and saving each as its own NIfTI image.
- `removeBackground.py`: Takes the per-region mask files and zeroes out every non-maximum value, leaving only the highest-intensity (white) pixels to isolate the organ foreground; writes the result as `_white_only.nii.gz`.
- `justOrgan.py`: Applies a binary mask from the `_white_only` files to the corresponding original scan, keeping only the masked organ intensities and forcing the background to black; saves outputs into `processed_images1`.
- `overlaid.py`: Overlays binary masks onto normalized versions of the original scans slice-by-slice using OpenCV blending, producing grayscale NIfTI overlays for visual QA.
- `processImages.py`: Performs slice-wise augmentation (flips, crops, affine transforms) on overlaid NIfTI volumes after normalization; saves augmented volumes to `processed_images_augmented`.
- `sliceThemUp.py`: Converts each masked NIfTI volume into normalized 2D PNG slices, creating one output folder per volume with numbered slice files.
- `sorted.py`: Renames PNG slices inside each region folder according to a predefined AMOS ID → modality mapping (e.g., `0001` → `CT_1`) to produce consistent modality prefixes.
- `actuallyShufflling.py`: Renames region folders themselves based on a provided mapping by using a two-step temp rename to avoid conflicts.
- `extraSorting.py`: Creates `region_1`…`region_12` folders and moves any file with `region_<n>` in its name into the matching folder.
- `randomizing.py`: Within every region folder, creates modality subfolders (`CT_*` and `MRI_*`) and moves slices into the matching modality folder based on filename prefixes.
- `helpSoTired.py`: Renames nested folders and PNG filenames by replacing a specific study identifier (e.g., `amos_0599`) with a new label (e.g., `MRI_3`) across a tree of region folders.
- `checkResolution.py`: Prints the pixel resolution of every PNG in a specified directory to validate slice dimensions.
- `imageviewer.py`: Loads a single NIfTI file and opens it in Napari for interactive inspection while printing volume dimensions and voxel spacing.
- `gettingScale.py`: Prints voxel dimensions, affine matrix, and array shape for a given NIfTI file and includes a helper to convert millimeter distances to pixel counts.
- `Data_Loader_for_Training.py`: Defines a PyTorch `Dataset` and `DataLoader` for grayscale TIFF slices with resize and normalization transforms; iterates through batches for quick sanity checks.

## Running the tools
1. Install dependencies such as `nibabel`, `numpy`, `opencv-python`, `Pillow`, `imgaug`, `torch`, `torchvision`, and `napari` in your Python environment.
2. Adjust the input and output paths at the top of each script to point to your AMOS data locations.
3. Execute scripts individually with `python <script_name>.py` to perform the corresponding processing or QA step.

## Purpose
These utilities streamline preparing the AMOS dataset for machine learning by extracting organ masks, cleaning backgrounds, generating visual overlays, augmenting data, and organizing consistent slice outputs ready for training pipelines.
