import ast
import astunparse
import re
import os

def parse_python(code):
    tree = ast.parse(code)
    return [astunparse.unparse(node).strip() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def parse_java(code):
    methods = []
    pattern = r'(public|private|protected|static)?\s+\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\}'
    for match in re.finditer(pattern, code):
        methods.append(match.group(0))
    return methods

def parse_cpp(code):
    methods = []
    pattern = r'(public|private|protected|static)?\s+\w+\s+\w+\s*\(.*?\)\s*\{.*?\}'
    for match in re.finditer(pattern, code, re.DOTALL):
        method = match.group(0).strip()
        methods.append(method)
    return methods

def parse_methods(file_path):
    _, extension = os.path.splitext(file_path)
    language_mapping = {
        '.py': parse_python,
        '.java': parse_java,
        '.cpp': parse_cpp
    }

    with open(file_path, 'r') as file:
        code = file.read()

    parse_function = language_mapping.get(extension)

    if parse_function:
        try:
            return parse_function(code)
        except Exception as e:
            print(f"Parsing error: {e}")

    # Default to chunks of 30 lines for unsupported extensions
    lines = code.split('\n')
    chunks = [lines[i:i + 30] for i in range(0, len(lines), 30)]
    return ['\n'.join(chunk) for chunk in chunks]
