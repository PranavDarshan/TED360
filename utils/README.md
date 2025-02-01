# Utility Files for Data Processing

## average_dimensions.py

Calculate the average width, length, and height for the object across all JSON files in a directory. Skips empty JSON files. Used to create the anchor box configs.

## bin_normalization.py

Used to normalize intensity values of wirin data from 0-1. The Ouster OS0 sensors generate a 16 bit value which needs to be normalised from 0-65,536 to 0-1.

## check_classes.py

Check the number and types of classes in the annotion values.

## generate_2d_projection.py

Creates x1, y1, x2, y2 values for the Ouster data. The values are derived from a projection onto the xy plane using the values of the x, y, rot_y values in the annotations and the camera projection matrix for the kitti dataset.
```ruby
# KITTI Camera Projection Matrix
P = np.array([
    [721.5377, 0, 609.5593, 44.85728],  
    [0, 721.5377, 172.854, 0.2163791],  
    [0, 0, 1, 0]
])
```

## pickler.py

Used to convert files to .pkl format.

## unpickle.py

Used to read data from .pkl files.
