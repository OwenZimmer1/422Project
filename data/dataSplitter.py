import os
import re

def split_methods(input_file, output_dir):
    """
    Splits Java methods from a single file into separate files,
    each named method1.txt, method2.txt, etc., inside a specified directory.

    Args:
        input_file (str): Path to the file containing all Java methods (allMethods.txt).
        output_dir (str): Path to the directory where the split files will be created (splitData).
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r') as file:
        content = file.read()

    # Regex to find Java methods based on Javadoc comments
    method_pattern = r'\/\*\*[\s\S]*?\*\/\s*.*?\)\s*\{[\s\S]*?\}'
    methods = re.findall(method_pattern, content)

    for i, method in enumerate(methods):
        output_file_path = os.path.join(output_dir, f'method{i+1}.txt')
        with open(output_file_path, 'w') as output_file:
            output_file.write(method)

if __name__ == '__main__':
    input_file = 'allMethods.txt'
    output_dir = 'splitData'
    split_methods(input_file, output_dir)
    print(f"Methods split and saved to {output_dir}")
