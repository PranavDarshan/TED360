# Python code used to visualize wirin data from ouster sensor
import numpy as np
import json
from mayavi import mlab

# Load point cloud data from .bin file
def load_point_cloud(bin_file):
    point_cloud = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)
    return point_cloud

# Load annotations from .json file
def load_annotations(json_file):
    with open(json_file, 'r') as f:
        annotations = json.load(f)
    return annotations["bounding boxes"]  # Extract "bounding boxes" list

# Visualize point cloud and annotations
def visualize_point_cloud_with_annotations(point_cloud, annotations):
    x, y, z = point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2]
    mlab.figure(bgcolor=(0, 0, 0), size=(800, 600))
    mlab.points3d(x, y, z, point_cloud[:, 3], mode="point", colormap="spectral", scale_factor=1)

    # Process bounding boxes from annotations
    for annotation in annotations:
        center = annotation["center"]
        width = annotation["width"]
        length = annotation["length"]
        height = annotation["height"]
        angle = annotation["angle"]  # Rotation of the bounding box (in radians)
        
        # Add 90-degree (π/2 radians) rotation to the bounding box
        angle += np.pi / 2  # Rotate by 90 degrees about the Z-axis

        # Compute and draw the bounding box
        draw_bbox(center, width, length, height, angle)

    mlab.show()

# Draw a bounding box given its center, dimensions, and rotation
def draw_bbox(center, width, length, height, angle):
    cx, cy, cz = center["x"], center["y"], center["z"]

    # Define the local coordinates of the bounding box corners
    local_corners = np.array([
        [-length / 2, -width / 2, -height / 2],
        [ length / 2, -width / 2, -height / 2],
        [ length / 2,  width / 2, -height / 2],
        [-length / 2,  width / 2, -height / 2],
        [-length / 2, -width / 2,  height / 2],
        [ length / 2, -width / 2,  height / 2],
        [ length / 2,  width / 2,  height / 2],
        [-length / 2,  width / 2,  height / 2]
    ])




    # Apply rotation around the Z-axis (yaw) with the additional 90-degree rotation
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0,              0,             1]

    ])
    rotated_corners = np.dot(local_corners, rotation_matrix.T)
    print(rotated_corners)
    # Translate the rotated corners to the center position
    global_corners = rotated_corners + np.array([cx, cy, cz])
    print(global_corners)
    # Define edges of the bounding box
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom face
        [4, 5], [5, 6], [6, 7], [7, 4],  # Top face
        [0, 4], [1, 5], [2, 6], [3, 7]   # Vertical edges
    ]

    # Draw each edge
    for edge in edges:
        line = global_corners[edge]
        mlab.plot3d(line[:, 0], line[:, 1], line[:, 2], color=(0, 1, 0), tube_radius=None, line_width=1.0)

# Main script
if __name__ == "__main__":
    bin_file = '000000.bin'
    json_file = 'wirin.json'

    point_cloud = load_point_cloud(bin_file)
    annotations = load_annotations(json_file)

    print("Annotations loaded:", annotations)  # Debug annotations
    visualize_point_cloud_with_annotations(point_cloud, annotations)
