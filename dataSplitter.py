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

method_count = 0
for part in parts:
    if part.strip() == "":
        continue

    full_method = "/**" + part.strip()

    # Separate Javadoc and the rest
    if "*/" in full_method:
        javadoc_end_index = full_method.index("*/") + 2
        javadoc = full_method[:javadoc_end_index].strip()
        code = full_method[javadoc_end_index:].strip()
    else:
        # Just in case something went wrong, skip this chunk
        continue

    method_count += 1
    filename = os.path.join(output_dir, f"method{method_count}.json")

    # Write as structured JSON
    with open(filename, "w") as f:
        json.dump({
            "javadoc": javadoc,
            "code": code
        }, f, indent=2)

print(f"{method_count} methods split with Javadoc/code and saved as JSON in {output_dir}.")
