import os
import json

# Directory containing the split JSON files
input_dir = "data/splitData"
output_file = "data/allMethodsCombined.json"

combined_methods = []

# Go through all .json files in the directory
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith(".json"):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r") as f:
            method_data = json.load(f)
            combined_methods.append(method_data)

# Save to one JSON file
with open(output_file, "w") as f:
    json.dump(combined_methods, f, indent=2)

print(f"Combined {len(combined_methods)} methods into {output_file}")
