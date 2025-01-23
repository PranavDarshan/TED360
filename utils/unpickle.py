# USES PYTHON 3
import pickle

# Replace 'your_file.pkl' with the path to your pickle file kitti_infos_test
filename = './example_rotation.pkl'

# Open the file in binary read mode
with open(filename, 'rb') as file:
    # Load the object from the file
    data = pickle.load(file)
# Now 'data' contains the un
# pickled object
print(data)
