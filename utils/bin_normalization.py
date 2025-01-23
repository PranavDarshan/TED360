# Wirin data is collected from ouster sensor intensity ranging from 0-65000. We normalize this data to be able to be compatible with kitti data for training.
import numpy as np
import os

# Folder containing the original .bin files
input_folder_path = "./Lidar Dataset for Students/Pcd/"

# Folder to save the modified .bin files
output_folder_path = "/data1/ted/TED/wirin_data/velodyne/"

# Define the data type (4 float32 values per point: x, y, z, intensity)
data_type = np.dtype([('x', 'float32'), ('y', 'float32'), ('z', 'float32'), ('intensity', 'float32')])

# Function to modify intensity values in a .bin file
def modify_intensity_in_bin(file_path, output_file_path):
    # Read the binary file
    data = np.fromfile(file_path, dtype=data_type)
    
    # Modify the intensity values by dividing them by 6500
    # Maximum value intensity found by ouster sensor for very bright objects is 6000
    data['intensity'] = data['intensity'] / 6500
    
    # Write the modified data to a new binary file
    data.tofile(output_file_path)
    print(f"Modified data written to: {output_file_path}")

# Ensure the output folder exists
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

list_files = [
    '63.592409180.bin',
    '455.574360300.bin',
    '654.907326050.bin',
    '2070.932538630.bin',
    '348.440927510.bin',
    '1970.940456830.bin',
    '257.421958380.bin',
    '236.878834780.bin',
    '3912.956195360.bin',
    '1692.481017630.bin',
    '1820.950152200.bin',
    '141.516695190.bin',
    '1564.967666400.bin',
    '2021-03-01-11-3BLR_IND_lidOFrame000200.bin',
    '1584.966396210.bin',
    '1527.892858930.bin',
    '106.219350630.bin',
    '657.907137240.bin',
    '2134.928052180.bin',
    '1255.031271130.bin',
    '237.878858750.bin',
    '531.626531560.bin',
    '531.626531560.bin',
    '682.904413220.bin',
    '758.998883500.bin',
    '137.016893510.bin',
    '639.908823080.bin',
    '2086.931437130.bin',
    '215.996857770.bin'
]

# Iterate through all the files in the input folder
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.bin'):
        if file_name in list_files:
            continue
        input_file_path = os.path.join(input_folder_path, file_name)
        output_file_path = os.path.join(output_folder_path, f"{file_name}")
        
        # Modify intensity in the file
        modify_intensity_in_bin(input_file_path, output_file_path)
