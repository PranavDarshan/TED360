# Generates the data x1 y1 x2 y2 for the ouster data
import os
import numpy as np

def read_kitti_labels(file_path):
    """Reads KITTI 3D bounding box annotations and extracts necessary parameters."""
    objects = []
    with open(file_path, 'r') as f:
        for line in f:
            values = line.strip().split()
            obj_class = values[0]
            truncated = float(values[1])
            occluded = float(values[2])
            alpha = float(values[3])
            x1, y1, x2, y2 = float(values[4]), float(values[5]), float(values[6]), float(values[7])
            height, width, length = float(values[8]), float(values[9]), float(values[10])
            x, y, z, rot_y = float(values[11]), float(values[12]), float(values[13]), float(values[14])

            objects.append({
                "class": obj_class,
                "truncated": truncated,
                "occluded": occluded,
                "alpha": alpha,
                "bbox_2d": (x1, y1, x2, y2),
                "dimensions": (height, width, length),
                "location": (x, y, z),
                "rotation_y": rot_y
            })
    return objects

def get_3d_corners(x, y, z, h, w, l, rot_y):
    """Computes the 8 corner points of a 3D bounding box in the camera coordinate system."""
    dx = l / 2
    dy = h / 2
    dz = w / 2

    corners = np.array([
        [dx, dy, dz],  [dx, dy, -dz],  [-dx, dy, -dz],  [-dx, dy, dz],  
        [dx, -dy, dz], [dx, -dy, -dz], [-dx, -dy, -dz], [-dx, -dy, dz]
    ])

    R = np.array([
        [np.cos(rot_y), 0, np.sin(rot_y)],
        [0, 1, 0],
        [-np.sin(rot_y), 0, np.cos(rot_y)]
    ])

    corners = np.dot(R, corners.T).T + np.array([x, y, z])
    return corners

def project_to_image(points_3d, P):
    """Projects 3D points to 2D image coordinates using the camera projection matrix."""
    points_3d_h = np.hstack((points_3d, np.ones((points_3d.shape[0], 1))))  
    points_2d = np.dot(P, points_3d_h.T)  
    points_2d = points_2d[:2] / points_2d[2]  
    return points_2d.T  

def compute_2d_bbox(obj, P):
    """Computes 2D bounding box (x1, y1, x2, y2) for a given 3D object."""
    x, y, z = obj["location"]
    h, w, l = obj["dimensions"]
    rot_y = obj["rotation_y"]

    corners_3d = get_3d_corners(x, y, z, h, w, l, rot_y)
    projected_corners = project_to_image(corners_3d, P)

    x1, y1 = np.min(projected_corners, axis=0)
    x2, y2 = np.max(projected_corners, axis=0)

    return x1, y1, x2, y2

def save_kitti_labels(output_path, objects, P):
    """Saves the updated KITTI labels with computed (x1, y1, x2, y2) values."""
    with open(output_path, 'w') as f:
        for obj in objects:
            x1, y1, x2, y2 = compute_2d_bbox(obj, P)
            f.write("{} {:.2f} {} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(
                obj['class'], 0.0, 0.0, 1,
                x1, y1, x2, y2,
                obj['dimensions'][0], obj['dimensions'][1], obj['dimensions'][2],
                obj['location'][0], obj['location'][1], obj['location'][2], obj['rotation_y']
            ))

def process_folder(input_folder, output_folder, P):
    """Processes all label files in the input folder and saves updated labels in the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    label_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]

    for file_name in label_files:
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        objects = read_kitti_labels(input_path)
        save_kitti_labels(output_path, objects, P)

        print("Processed:", file_name)

# KITTI Camera Projection Matrix
P = np.array([
    [721.5377, 0, 609.5593, 44.85728],  
    [0, 721.5377, 172.854, 0.2163791],  
    [0, 0, 1, 0]
])

input_folder = './label_2_original/'
output_folder = './label_2_mod/'

# Process all label files
process_folder(input_folder, output_folder, P)

print("Processing complete. Updated labels saved in:", output_folder)
