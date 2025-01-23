import numpy as np
import json
from mayavi import mlab

# Load point cloud data from .bin file
def load_point_cloud(bin_file):
    point_cloud = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)
    return point_cloud

# Load annotations from .json file
def load_annotations(label_file):
      with open(label_file, 'r') as f:
            labels = f.readlines()
      return labels  # Extract "bounding boxes" list

# Visualize point cloud and annotations
def visualize_point_cloud_with_annotations(point_cloud, labels):
    x, y, z = point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2]
    mlab.figure(bgcolor=(0, 0, 0), size=(800, 600))
    mlab.points3d(x, y, z, point_cloud[:, 3], mode="point", colormap="spectral", scale_factor=1)

    # Process bounding boxes from annotations
    for line in labels:
        line = line.split()
        lab, _, _, _, _, _, _, _, h, w, l, x, y, z, rot = line
        # Example usage
        # angle_deg = 120
        print(h, w, l, x, y, z, rot)
        h, w, l, x, y, z, rot = map(float, [h, w, l, x, y, z, rot])
        
        # Add 90-degree (π/2 radians) rotation to the bounding box
        #x_corners = [l / 2, l / 2, -l / 2, -l / 2, l / 2, l / 2, -l / 2, -l / 2]
        #y_corners = [0, 0, 0, 0, -h, -h, -h, -h]
        #z_corners = [w / 2, -w / 2, -w / 2, w / 2, w / 2, -w / 2, -w / 2, w / 2]
        #corners_3d = np.vstack([x_corners, y_corners, z_corners])  # (3, 8)

        # Compute and draw the bounding box
        draw_bbox(x,y,z, w, l, h, rot)

    mlab.show()

# Draw a bounding box given its center, dimensions, and rotation
def draw_bbox(x,y,z, w, l, h, rot):
    
    # Define the local coordinates of the bounding box corners
    x_corners = [l / 2, l / 2, -l / 2, -l / 2, l / 2, l / 2, -l / 2, -l / 2]
    y_corners = [0, 0, 0, 0, -h, -h, -h, -h]
    z_corners = [w / 2, -w / 2, -w / 2, w / 2, w / 2, -w / 2, -w / 2, w / 2]
    corners_3d = np.vstack([x_corners, y_corners, z_corners])
    # Apply rotation around the Z-axis (yaw) with the additional 90-degree rotation
    rotation_matrix = np.array([
        [np.cos(rot), -np.sin(rot), 0],
        [np.sin(rot),  np.cos(rot), 0],
        [0,              0,             1]

    ])

    R = np.array([[np.cos(rot), 0, np.sin(rot)],
                    [0, 1, 0],
                    [-np.sin(rot), 0, np.cos(rot)]])
    corners_3d = np.dot(R, corners_3d).T  + np.array([x, y, z])

    corners_3d = corners_3d[:, [2, 0, 1]] * np.array([[1, -1, -1]])
    print(corners_3d)
    # Translate the rotated corners to the center position
    

    # Define edges of the bounding box
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom face
        [4, 5], [5, 6], [6, 7], [7, 4],  # Top face
        [0, 4], [1, 5], [2, 6], [3, 7]   # Vertical edges
    ]

    # Draw each edge
    for edge in edges:
        line = corners_3d[edge]
        mlab.plot3d(line[:, 0], line[:, 1], line[:, 2], color=(0, 1, 0), tube_radius=None, line_width=1.0)

# Main script
if __name__ == "__main__":
    bin_file = '000000.bin'
    json_file = '000000.txt'

    point_cloud = load_point_cloud(bin_file)
    annotations = load_annotations(json_file)

    print("Annotations loaded:", annotations)  # Debug annotations
    visualize_point_cloud_with_annotations(point_cloud, annotations)
