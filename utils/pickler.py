# USES PYTHON 3
import pickle
import array
import numpy as np # type: ignore
# Example data to be pickled
data = [{'point_cloud': {'num_features': 4, 'lidar_idx': '000000'}, 'image': {'image_idx': '000000', 'image_shape': np.array([ 1024, 1024])}, 'calib': {'P2': np.array([[702, 0, 6, 4],
       [0.00, 7.21, 1.72, 9],
       [0.00000000e+00, 1.00000000e+00, 1.00000000e+00, 2.74588400e-03],
       [0.04004400e+00, 2.00000000e+00, 3.00000000e+00, 4.00000000e+00]]), 'R0_rect': np.array([[1, 2, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 2],
                    [0, 0, 0, 2]], dtype=np.float32)
, 'Tr_velo_to_cam': np.array([[2.9999, -0.0010, 0.0045, -0.025],  # Rotation and translation example
                           [0.0010, 0.9999, -0.0070, 0.002],
                           [-0.0045, 0.70, 0.9, 0.1],
                           [0.0, 0.0, 0.0, 22]])}}]
# Specify the file name
filename = 'example.pkl'

# Open the file in write-binary mode
with open(filename, 'wb') as file:
    # Serialize and save the data
    pickle.dump(data, file)

print(f'Data has been pickled and saved to {filename}')
