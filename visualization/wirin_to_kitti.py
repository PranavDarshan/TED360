# Python script to change annotations from wirin axis to kitti axis.
# Reads annotations data from a json file and updates to text file.
import os
import numpy as np
import json

def global_to_kitti(json_file, kitti_file):
    """
    Convert bounding boxes from global coordinates (JSON) to KITTI format.
    """
    try:
        with open(json_file, 'r') as f:
            annotations = json.load(f).get("bounding boxes", [])
        
        kitti_annotations = []

        for annotation in annotations:
            class1 = annotation.get("object_id")
            center = annotation.get("center", {})
            width = annotation.get("width")
            length = annotation.get("length")
            height = annotation.get("height")
            angle = annotation.get("angle", 0.0)  # Default rotation to 0 if missing
            
            # Validate and parse center and height
            if not center or not all(k in center for k in ["y", "z", "x"]) or height is None:
                print(f"Skipping invalid annotation in {json_file}")
                continue

            try:
                camera_center = np.array([-center["y"], -center["z"]+(height/2), center["x"]])
                
                
            except (TypeError, ValueError):
                print(f"Error processing annotation: {annotation} in {json_file}")
                continue

            # Convert angle and format dimensions
            kitti_angle = -angle
            kitti_length, kitti_width, kitti_height = length, width, height

            # KITTI annotation string
            kitti_annotations.append(
                f"{class1} 0.0 0.0 -1.0 0.0 0.0 0.0 0.0 "
                f"{kitti_height:.2f} {kitti_width:.2f} {kitti_length:.2f} "
                f"{camera_center[0]:.2f} {camera_center[1]:.2f} {camera_center[2]:.2f} {kitti_angle:.2f}"
            )

        # Write to KITTI file
        with open(kitti_file, 'w') as f:
            f.write("\n".join(kitti_annotations))
    except Exception as e:
        print(f"Failed to process {json_file}: {e}")

def convert_directory(json_dir, kitti_dir):
    """
    Convert all JSON files in a directory to KITTI format.
    """
    os.makedirs(kitti_dir, exist_ok=True)
    for file_name in os.listdir(json_dir):
        if file_name.endswith(".json"):
            json_file = os.path.join(json_dir, file_name)
            kitti_file = os.path.join(kitti_dir, file_name.replace(".json", ".txt"))
            #print(f"Converting {json_file} to {kitti_file}")
            global_to_kitti(json_file, kitti_file)

if __name__ == "__main__":
    json_directory = "./Lidar Dataset for Students/Json/"
    kitti_directory = "/data1/ted/TED/new_json"

    convert_directory(json_directory, kitti_directory)
    print("finished conversion")
