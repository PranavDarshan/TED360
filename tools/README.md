# Tools for Training

The test.py has been changed for including 6 classes. The config files - kitti_dataset.yaml and TED-S.yaml have been changed for including six classes.

## test.py

Used to rotate the lidar points 120 degress about the z axis. This code creates 2 new files of the same file which are rotated by 120 and 240 degrees. This is done to run inference 3 times and finally the annotation predictions are stitched together.

```ruby
def rotate_points(points, angle_degrees):
    # Convert angle to radians
    angle_radians = np.radians(angle_degrees)
    
    # Create the rotation matrix for the XY plane
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians)],
        [np.sin(angle_radians), np.cos(angle_radians)]
    ])
    
    # Rotate the x and y coordinates
    xy_rotated = np.dot(points[:, :2], rotation_matrix.T)
    
    # Keep z and intensity values the same
    rotated_points = np.hstack((xy_rotated, points[:, 2:]))
    
    return rotated_points
```

Code in the test.py runs inference 3 times where for each file, the points are rotated and then saved in the same directory and then they are used to run inference.
```ruby
    # Load the original point cloud data
    file_path = os.path.join(preferred_directory, '000000.bin')
    points = load_bin_file(file_path)

    # Rotate 120 degrees clockwise (negative angle)
    points_clockwise = rotate_points(points, -120)
    save_bin_file(points_clockwise, os.path.join(preferred_directory, '000001.bin'))

    # Rotate 120 degrees counterclockwise (positive angle)
    points_counterclockwise = rotate_points(points, 120)
    save_bin_file(points_counterclockwise, os.path.join(preferred_directory, '000002.bin'))
```

## kitti_dataset.yaml

INFO_PATH for testing has been changed and the model evaluates on the image indexes present in the example_rotation.pkl.

```ruby
INFO_PATH: {
    'train': [kitti_infos_train.pkl],
    'test': [example_rotation.pkl],
}
```

## TES-S.yaml

New classes are added 'Car', 'Pedestrian', 'Cyclist', 'Motorcyclist', 'Truck', 'Bus' to suit the Indian roads.
```ruby
CLASS_NAMES: ['Car', 'Pedestrian', 'Cyclist', 'Motorcyclist', 'Truck', 'Bus']
```

Anchor boxes for the new classes are added.
```ruby
ANCHOR_GENERATOR_CONFIG = [
    {
        'class_name': 'Car',
        'anchor_sizes': [[3.9, 1.6, 1.56]],
        'anchor_rotations': [0, 1.57],
        'anchor_bottom_heights': [-1.78],
        'align_center': False,
        'feature_map_stride': 8,
        'matched_threshold': 0.6,
        'unmatched_threshold': 0.45
    },
    {
        'class_name': 'Pedestrian',
        'anchor_sizes': [[0.8, 0.6, 1.73]],
        'anchor_rotations': [0, 1.57],
        'anchor_bottom_heights': [-0.6],
        'align_center': False,
        'feature_map_stride': 8,
        'matched_threshold': 0.5,
        'unmatched_threshold': 0.35
    },
    {
        'class_name': 'Cyclist',
        'anchor_sizes': [[1.76, 0.6, 1.73]],
        'anchor_rotations': [0, 1.57],
        'anchor_bottom_heights': [-0.6],
        'align_center': False,
        'feature_map_stride': 8,
        'matched_threshold': 0.5,
        'unmatched_threshold': 0.35
    },
    {
        'class_name': 'Motorcyclist',
        'anchor_sizes': [[1.6, 1.2, 1.6]], 
        'anchor_rotations': [0, 1.57],
        'anchor_bottom_heights': [-0.6], 
        'align_center': False,
        'feature_map_stride': 8,
        'matched_threshold': 0.5,
        'unmatched_threshold': 0.35
    },
    {
        'class_name': 'Truck',
        'anchor_sizes': [[4.8, 2.8, 3]], 
        'anchor_rotations': [0, 1.57],
        'anchor_bottom_heights': [-1.5], 
        'align_center': False,
        'feature_map_stride': 8,
        'matched_threshold': 0.6,
        'unmatched_threshold': 0.45
    },
    {
        'class_name': 'Bus',
        'anchor_sizes': [[9.0, 3.0, 3.8]],
        'anchor_rotations': [0, 1.57],
        'anchor_bottom_heights': [-1.5], 
        'align_center': False,
        'feature_map_stride': 8,
        'matched_threshold': 0.6,
        'unmatched_threshold': 0.45
    }
]

```
