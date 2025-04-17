import os
import json

# File paths
input_path = "data/allMethods.txt"
output_dir = "data/splitData"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read input content
with open(input_path, "r") as f:
    content = f.read()

# Split the content by each Javadoc start
parts = content.split("/**")

# Write each method into a JSON file
method_count = 0
for part in parts:
    if part.strip() == "":
        continue

    method = "/**" + part.strip()
    method_count += 1
    filename = os.path.join(output_dir, f"method{method_count}.json")

    # Wrap in a JSON object
    with open(filename, "w") as f:
        json.dump({"method": method}, f, indent=2)

print(f"{method_count} methods split and saved to {output_dir} as JSON.")
