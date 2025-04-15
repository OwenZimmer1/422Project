import os

# File paths
input_path = "data/allMethods.txt"
output_dir = "data/splitData"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read input content
with open(input_path, "r") as f:
    content = f.read()

# Split the content by each Javadoc start, keeping splits clean
parts = content.split("/**")

# The first split might be empty or contain junk before the first method
method_count = 0
for part in parts:
    if part.strip() == "":
        continue  # Skip empty or pre-method content

    method = "/**" + part.strip()  # Add back the removed Javadoc start
    method_count += 1
    filename = os.path.join(output_dir, f"method{method_count}.txt")

    with open(filename, "w") as f:
        f.write(method)

print(f"{method_count} methods split and saved to {output_dir}")
