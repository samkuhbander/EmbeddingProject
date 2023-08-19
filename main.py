import ast
import os
import astunparse
import glob

def parse_python(code):
    tree = ast.parse(code)
    return [astunparse.unparse(node).strip() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def parse_methods(file_path):
    _, extension = os.path.splitext(file_path)
    language_mapping = {
        '.py': parse_python,
    }

    with open(file_path, 'r') as file:
        code = file.read()

    parse_function = language_mapping.get(extension)

    try:
        if parse_function:
            return parse_function(code)

    except Exception as e:
        print(f"Parsing error: {e}")

    # Default behavior for other or unknown languages, or if parsing failed
    lines = code.split('\n')
    chunks = [lines[i:i + 20] for i in range(0, len(lines), 20)]
    return ['\n'.join(chunk) for chunk in chunks]

directory_path = 'ExampleProject/*'  # Adjust with the directory path you want to parse
files = glob.glob(directory_path)

for file_path in files:
    print(f"Parsing file: {file_path}")
    methods_or_chunks = parse_methods(file_path)
    for index, method_or_chunk in enumerate(methods_or_chunks):
        print(f"Chunk {index + 1}:")
        print(method_or_chunk)
        print("-" * 50)  # Separator line
