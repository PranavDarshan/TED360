import os
import json

def parse_json_files(folder_path):
    distinct_object_ids = set() 
    

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):  # Check if the file is a JSON file
            file_path = os.path.join(folder_path, filename)
            

            with open(file_path, 'r') as f:
                data = json.load(f)
                

                bounding_boxes = data.get("bounding boxes", [])
                

                for box in bounding_boxes:
                    object_id = box.get("object_id")
                    if object_id:
                        distinct_object_ids.add(object_id)
    
    return distinct_object_ids


folder_path = '/data3/Lidar Dataset for Students/Json'


object_ids = parse_json_files(folder_path)
print("Distinct object IDs:", object_ids)
