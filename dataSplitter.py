import os
import json
import re

input_path = "data/allMethods.txt"
output_dir = "data/splitData"
os.makedirs(output_dir, exist_ok=True)

with open(input_path, "r") as f:
    content = f.read()

parts = content.split("/**")

method_count = 0
for part in parts:
    if part.strip() == "":
        continue

    full_method = "/**" + part.strip()
    if "*/" not in full_method:
        continue

    javadoc_end_index = full_method.index("*/") + 2
    javadoc = full_method[:javadoc_end_index].strip()
    code = full_method[javadoc_end_index:].strip()

    # Match the method signature
    signature_match = re.match(r"(public|private|protected)?\s*(static)?\s*([\w<>\[\]]+)\s+(\w+)\s*\(", code)
    if signature_match:
        access_modifier = signature_match.group(1) or "default"
        return_type = signature_match.group(3)
        method_name = signature_match.group(4)
    else:
        access_modifier = return_type = method_name = "unknown"

    method_count += 1
    filename = os.path.join(output_dir, f"method{method_count}.json")
    with open(filename, "w") as f:
        json.dump({
            "javadoc": javadoc,
            "code": code,
            "accessModifier": access_modifier,
            "returnType": return_type,
            "methodName": method_name
        }, f, indent=2)

print(f"{method_count} methods split and saved with extra metadata.")
