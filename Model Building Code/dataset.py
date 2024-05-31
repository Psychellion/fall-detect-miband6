import h5py
import numpy as np
from skimage import io

# Define your data paths
rgb_train_paths = ["THESIS FINAL OUTPUTS/fall_dataset/images/train/fall001.jpg", "THESIS FINAL OUTPUTS/fall_dataset/images/train/fall002.jpg", ...]
labels_train = [0, 1, 0, ...]  # Example labels

rgb_val_paths = ["THESIS FINAL OUTPUTS/fall_dataset/images/val/fall001.jpg", "THESIS FINAL OUTPUTS/fall_dataset/images/val/fall002.jpg", ...]
labels_val = [0, 1, 0, ...]

# Read images and convert them to numpy arrays
def load_images(paths):
    images = [io.imread(path) for path in paths]
    return np.array(images)

# Load training and validation data
X_rgb_train = load_images(rgb_train_paths)
y_train = np.array(labels_train)

X_rgb_val = load_images(rgb_val_paths)
y_val = np.array(labels_val)

# Create HDF5 file
with h5py.File("FallDetectionDataset/video.hdf5", "w") as f:
    # Create groups
    data_group = f.create_group("data")
    labels_group = f.create_group("labels")

    # Create subgroups for training and validation data
    rgb_group = data_group.create_group("rgb")
    mhi_group = data_group.create_group("mhi")

    rgb_train_dataset = rgb_group.create_dataset("train", data=X_rgb_train, compression="gzip")
    labels_train_dataset = labels_group.create_dataset("train", data=y_train, compression="gzip")

    rgb_val_dataset = rgb_group.create_dataset("val", data=X_rgb_val, compression="gzip")
    labels_val_dataset = labels_group.create_dataset("val", data=y_val, compression="gzip")
