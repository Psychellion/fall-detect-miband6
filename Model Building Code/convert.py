import cv2
import h5py
import numpy as np

def mp4_to_hdf5(input_video_path, output_hdf5_path):
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create HDF5 file
    with h5py.File(output_hdf5_path, 'w') as hf:
        video_data = hf.create_dataset('video', (frame_count, height, width, 3), dtype='uint8')
        
        idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Save frame to HDF5
            video_data[idx] = frame_rgb
            idx += 1

        print(f"Video converted successfully. Total frames: {frame_count}")

    cap.release()

if __name__ == "__main__":
    input_video_path = "D:\GLYCELLE\THESIS FINAL OUTPUTS\System Code\Model Building Code\train.mp4"
    output_hdf5_path = "output_video.h5"
    mp4_to_hdf5(input_video_path, output_hdf5_path)
