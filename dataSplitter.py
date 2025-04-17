import os
import json
import re

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

    # Separate Javadoc and code
    if "*/" in full_method:
        javadoc_end_index = full_method.index("*/") + 2
        javadoc = full_method[:javadoc_end_index].strip()
        code = full_method[javadoc_end_index:].strip()
    else:
        continue

    # Extract method signature details
    signature_match = re.search(
        r"(?:public|private|protected)?\s*(?:static\s+)?([a-zA-Z0-9_<>\[\]]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)",
        code
    )

    if signature_match:
        return_type = signature_match.group(1)
        method_name = signature_match.group(2)
        parameters = signature_match.group(3).strip()
    else:
        return_type = "unknown"
        method_name = "unknown"
        parameters = ""

    # Extract return variable
    return_match = re.search(r"\breturn\s+([^;]+);", code)
    return_variable = return_match.group(1).strip() if return_match else ""

    # Extract called methods
    called_methods = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    keywords = {
        "if", "for", "while", "switch", "catch", "return", "new", "throw", "super", "this", "else", "try", "case"
    }
    called_methods = [m for m in called_methods if m not in keywords and m != method_name]
    seen = set()
    called_methods = [m for m in called_methods if not (m in seen or seen.add(m))]

    # Extract local variables
    local_var_matches = re.findall(
        r"\b([a-zA-Z0-9_<>\[\]]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?==|;)", code
    )
    local_variables = [var_name for _, var_name in local_var_matches]

    # Extract thrown exceptions
    thrown_matches = re.findall(r"throw\s+new\s+([A-Z][a-zA-Z0-9_]*)\s*\(", code)
    thrown_exceptions = list(set(thrown_matches))  # unique list

    method_count += 1
    filename = os.path.join(output_dir, f"method{method_count}.json")

    with open(filename, "w") as f:
        json.dump({
            "javadoc": javadoc,
            "code": code,
            "method_name": method_name,
            "parameters": parameters,
            "return_type": return_type,
            "return_variable": return_variable,
            "called_methods": called_methods,
            "local_variables": local_variables,
            "thrown_exceptions": thrown_exceptions
        }, f, indent=2)

print(f"{method_count} methods parsed with exception detection.")
