#!/usr/bin/env python3
"""
# Location Tag Generator

**File Tags**: #type/code-file
**Inheritable Tags**: #domain/automation #layer/infrastructure #category/code-generation

## Purpose
Automatically adds location tags to Python files based on their path.

Location tags follow the format:
  #location/code-file/DIRECTORY/STRUCTURE/HERE/filename.py

This tag is added to the **Inheritable Tags** line so that both the Python file
and all its AST children share the same location tag, making it easy to find
all code objects within a specific file.

Usage:
    python add_location_tags.py
    uv run add_location_tags.py
"""

import re
from pathlib import Path


def generate_location_tag(filepath: Path, root_dir: Path) -> str:
    """Generate location tag from file path.

    Examples:
        code/calculator.py -> #location/code-file/code/calculator.py
        code/test_operations.py -> #location/code-file/code/test_operations.py
    """
    rel_path = filepath.relative_to(root_dir)
    # Convert path to tag format (use forward slashes)
    path_str = str(rel_path).replace('\\', '/')
    return f"location/code-file/{path_str}"


def add_location_tag_to_file(filepath: Path, root_dir: Path) -> bool:
    """Add or update location tag in Python file's Inheritable Tags line.

    Returns:
        True if file was modified, False otherwise
    """
    content = filepath.read_text(encoding='utf-8')

    # Extract the docstring
    docstring_match = re.match(r'^(#!/usr/bin/env python3\n)?\s*"""(.*?)"""\s*\n', content, re.DOTALL)
    if not docstring_match:
        print(f"  WARNING: {filepath.name} has no docstring, skipping")
        return False

    shebang = docstring_match.group(1) or ''
    docstring = docstring_match.group(2)
    rest_of_file = content[docstring_match.end():]

    # Generate location tag
    location_tag = generate_location_tag(filepath, root_dir)

    # Find Inheritable Tags line
    inheritable_match = re.search(r'(\*\*Inheritable Tags\*\*:\s*)([^\n]+)', docstring)

    if not inheritable_match:
        print(f"  WARNING: {filepath.name} has no **Inheritable Tags**: line, skipping")
        return False

    prefix = inheritable_match.group(1)
    current_tags = inheritable_match.group(2)

    # Remove any existing location tag
    tags_cleaned = re.sub(r'#location/code-file/[^\s#]+\s*', '', current_tags).strip()

    # Add new location tag at the beginning
    new_tags = f"#{location_tag} {tags_cleaned}"

    # Check if already has this exact tag
    if f"#{location_tag}" in current_tags:
        # Already has correct location tag
        return False

    # Replace the line
    new_inheritable_line = f"{prefix}{new_tags}"
    new_docstring = docstring[:inheritable_match.start()] + new_inheritable_line + docstring[inheritable_match.end():]

    # Reconstruct file
    new_content = f'{shebang}"""{new_docstring}"""\n{rest_of_file}'

    filepath.write_text(new_content, encoding='utf-8')
    return True


def main():
    # Script is in maintenance_scripts/, root is parent
    root_dir = Path(__file__).parent.parent
    code_dir = root_dir / "code"

    print("=" * 60)
    print("Location Tag Generator")
    print("=" * 60)
    print()
    print(f"Root directory: {root_dir}")
    print(f"Code directory: {code_dir}")
    print()

    # Find all Python files
    python_files = list(code_dir.rglob("*.py"))

    if not python_files:
        print(f"No Python files found in {code_dir}")
        return

    print(f"Found {len(python_files)} Python files")
    print()

    modified_count = 0
    for py_file in sorted(python_files):
        rel_path = py_file.relative_to(root_dir)
        location_tag = generate_location_tag(py_file, root_dir)

        if add_location_tag_to_file(py_file, root_dir):
            print(f"  + {rel_path}: Added #{location_tag}")
            modified_count += 1
        else:
            print(f"  - {rel_path}: Already has correct location tag")

    print()
    print(f"Modified {modified_count} file(s)")
    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
