import os
import json
import numpy as np

def calculate_average_motorcyclist_dimensions(json_dir):
    """
    Calculate the average width, length, and height for the 'Motorcyclist' object across all JSON files in a directory.
    
    Skips empty JSON files.

    Parameters:
        json_dir (str): Path to the directory containing JSON files.

    Returns:
        tuple: Average width, length, and height of 'Motorcyclist' objects.
    """
    widths = []
    lengths = []
    heights = []
    
    # Iterate through all JSON files in the directory
    for file_name in os.listdir(json_dir):
        if file_name.endswith(".json"):
            json_file = os.path.join(json_dir, file_name)
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    
                    # Skip empty JSON files
                    if not data or "bounding boxes" not in data:
                        print(f"Skipping empty or invalid file: {file_name}")
                        continue

                    # Check for 'Motorcyclist' object in each file
                    for annotation in data.get("bounding boxes", []):
                        if annotation["object_id"] == "Motorcyclist":
                            width = annotation.get("width")
                            length = annotation.get("length")
                            height = annotation.get("height")

                            # Ensure the dimensions are valid (i.e., not None and are numbers)
                            if width is not None and isinstance(width, (int, float)):
                                widths.append(width)
                            if length is not None and isinstance(length, (int, float)):
                                lengths.append(length)
                            if height is not None and isinstance(height, (int, float)):
                                heights.append(height)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {file_name}")
                continue
    
    # Calculate the averages
    avg_width = np.mean(widths) if widths else 0
    avg_length = np.mean(lengths) if lengths else 0
    avg_height = np.mean(heights) if heights else 0
    
    return avg_width, avg_length, avg_height

# Example usage
if __name__ == "__main__":
    json_directory = "/data3/Lidar Dataset for Students/Json"  # Path to your JSON directory
    avg_width, avg_length, avg_height = calculate_average_motorcyclist_dimensions(json_directory)
    
    print(f"Average Motorcyclist Dimensions:\nWidth: {avg_width:.2f} m\nLength: {avg_length:.2f} m\nHeight: {avg_height:.2f} m")
