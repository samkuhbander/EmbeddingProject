import ast
import astunparse
import re

def parse_python(code):
    tree = ast.parse(code)
    return [astunparse.unparse(node).strip() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def parse_java(code):
    methods = []
    for match in re.finditer(r'(public|private|protected|static)?\s+\w+\s+\w+\s*\(.*\)\s*{[^}]*}', code):
        methods.append(match.group(0))
    return methods

def parse_cpp(code):
    methods = []
    pattern = r'(public|private|protected|static)?\s+\w+\s+\w+\s*\(.*?\)\s*\{.*?\}'
    for match in re.finditer(pattern, code, re.DOTALL):
        method = match.group(0).strip()
        methods.append(method)
    return methods
