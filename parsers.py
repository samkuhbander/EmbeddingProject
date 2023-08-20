import re
import os
import ast
import astunparse
from concurrent.futures import ThreadPoolExecutor

def parse_python(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            yield astunparse.unparse(node).strip()

def parse_java(code):
    pattern = re.compile(r'(public|private|protected|static)?\s+\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\}')
    for match in pattern.finditer(code):
        yield match.group(0)

def parse_cpp(code):
    pattern = re.compile(r'(public|private|protected|static)?\s+\w+\s+\w+\s*\(.*?\)\s*\{.*?\}', re.DOTALL)
    for match in pattern.finditer(code):
        yield match.group(0).strip()

def parse_file(file_path):
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
            return list(parse_function(code))
        except Exception as e:
            print(f"Parsing error in {file_path}: {e}")

    # Default to chunks of 30 lines for unsupported extensions
    lines = code.split('\n')
    chunks = [lines[i:i + 30] for i in range(0, len(lines), 30)]
    return ['\n'.join(chunk) for chunk in chunks]

def parse_multiple_files(files):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(parse_file, files))
