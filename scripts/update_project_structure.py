import os
import sys

def get_structure(startpath):
    structure = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f'{subindent}{f}')
    return structure

def create_project_structure_md():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(project_root, 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    structure = get_structure(project_root)
    with open(os.path.join(docs_dir, 'PROJECT_STRUCTURE.md'), 'w') as f:
        f.write("# Project Structure\n\n")
        f.write("```\n")
        f.write("\n".join(structure))
        f.write("\n```\n")
    print("PROJECT_STRUCTURE.md has been created/updated in the docs folder.")

if __name__ == "__main__":
    create_project_structure_md()
