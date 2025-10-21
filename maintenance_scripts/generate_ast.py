#!/usr/bin/env python3
"""
# AST Cache Generator

**Tags**: #type/code-file #domain/automation #layer/infrastructure #category/code-generation

## Purpose
Generate AST cache for Python files in the repository.

This script:
1. Adds Obsidian block reference markers to Python source code
2. Creates one Markdown AST file per Python object (function/class/method)
3. Builds an execution graph showing how Python interpreter sees relationships

**CRITICAL**: This generates custom AST format (not standard Python AST) that
includes our superset extensions: schematic functions, behavior references, and
object-level wikilinks.

Usage:
    python generate_ast.py              # Regenerate all
    python generate_ast.py --clean      # Clean and regenerate
    python generate_ast.py --no-markers # Don't modify source files
"""

import ast
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple


class BlockMarkerAdder(ast.NodeTransformer):
    """Add block reference markers to Python source code."""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.markers_added: List[Tuple[int, str]] = []  # (line_num, marker)

    def add_marker(self, node: ast.AST, marker: str):
        """Add a block marker to a specific line if not already present."""
        if not hasattr(node, 'lineno'):
            return

        lineno = node.lineno - 1  # Convert to 0-indexed
        if lineno >= len(self.source_lines):
            return

        line = self.source_lines[lineno]

        # Check if marker already exists
        if f"# ^{marker}" in line:
            return

        # Add marker at end of line (before any existing comment)
        stripped = line.rstrip()

        # If there's already a comment, insert before it
        if '#' in stripped and not stripped.strip().startswith('#'):
            # Find the first # that's not in a string
            comment_pos = stripped.find('#')
            self.source_lines[lineno] = (
                stripped[:comment_pos].rstrip() +
                f"  # ^{marker} " +
                stripped[comment_pos:] +
                '\n' if line.endswith('\n') else ''
            )
        else:
            # No existing comment, just append
            self.source_lines[lineno] = stripped + f"  # ^{marker}\n"

        self.markers_added.append((lineno + 1, marker))


def add_block_markers_to_source(source_code: str) -> Tuple[str, List[str]]:
    """Add Obsidian block reference markers to Python source code.

    Returns:
        (modified_source, list_of_markers_added)
    """
    lines = source_code.split('\n')
    tree = ast.parse(source_code)

    markers_to_add: List[Tuple[int, str]] = []  # (lineno, marker)

    # Walk AST and collect markers to add
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Top-level function or method
            parent_class = None

            # Check if this function is inside a class
            for parent in ast.walk(tree):
                if isinstance(parent, ast.ClassDef):
                    if node in ast.walk(parent):
                        # Check if direct child (not nested deeper)
                        if node in parent.body:
                            parent_class = parent.name
                            break

            if parent_class:
                marker = f"{parent_class}-{node.name}"
            else:
                marker = node.name

            markers_to_add.append((node.lineno, marker))

        elif isinstance(node, ast.ClassDef):
            marker = node.name
            markers_to_add.append((node.lineno, marker))

        elif isinstance(node, ast.Assign):
            # Module-level constants (ALL_CAPS)
            if hasattr(node, 'lineno') and node.lineno is not None:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if name.isupper() and len(name) > 1:
                            markers_to_add.append((node.lineno, name))

    # Sort by line number (reverse) to add from bottom up (preserves line numbers)
    markers_to_add.sort(reverse=True)

    # Add markers to source
    added_markers = []
    for lineno, marker in markers_to_add:
        idx = lineno - 1  # Convert to 0-indexed
        if idx >= len(lines):
            continue

        line = lines[idx]

        # Check if marker already exists
        if f"# ^{marker}" in line:
            continue

        # Add marker at end of line
        stripped = line.rstrip()

        # If there's already a comment, insert before it
        if '#' in stripped and not stripped.strip().startswith('#'):
            comment_pos = stripped.find('#')
            lines[idx] = (
                stripped[:comment_pos].rstrip() +
                f"  # ^{marker} " +
                stripped[comment_pos:]
            )
        else:
            # No existing comment, just append
            lines[idx] = stripped + f"  # ^{marker}"

        added_markers.append(marker)

    return '\n'.join(lines), added_markers


class ASTGenerator:
    """Generate custom AST cache as Obsidian-compatible Markdown files.

    Creates one .ast.md file per Python object (function/class/method).
    """

    def __init__(self, root_dir: Path, add_markers: bool = True):
        self.root_dir = root_dir
        self.code_dir = root_dir / "code"
        self.ast_cache_dir = root_dir / "ast-cache"
        self.metadata_file = self.ast_cache_dir / "metadata.json"
        self.add_markers = add_markers

    def generate_all(self, clean: bool = False):
        """Generate AST cache for all Python files."""
        if clean and self.ast_cache_dir.exists():
            print(f"Cleaning existing AST cache: {self.ast_cache_dir}")
            import shutil
            shutil.rmtree(self.ast_cache_dir)

        # Create ast-cache directory structure
        self.ast_cache_dir.mkdir(exist_ok=True)

        # Find all Python files
        python_files = list(self.code_dir.rglob("*.py"))

        if not python_files:
            print(f"No Python files found in {self.code_dir}")
            return

        print(f"Found {len(python_files)} Python files")

        # Generate AST for each file
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "generator_version": "2.0.0",
            "files": {}
        }

        for py_file in python_files:
            try:
                file_metadata = self.generate_ast_for_file(py_file)
                metadata["files"][str(py_file.relative_to(self.root_dir))] = file_metadata
                print(f"  Generated: {py_file.relative_to(self.root_dir)}")
            except Exception as e:
                print(f"  ERROR: {py_file.relative_to(self.root_dir)}: {e}")
                import traceback
                traceback.print_exc()

        # Write metadata
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        print(f"\nAST cache generated in: {self.ast_cache_dir}")
        print(f"Metadata: {self.metadata_file}")

    def generate_ast_for_file(self, py_file: Path) -> Dict[str, Any]:
        """Generate AST markdown files for all objects in a Python file."""
        # Read source
        source = py_file.read_text(encoding='utf-8')
        original_hash = hashlib.sha256(source.encode('utf-8')).hexdigest()

        # Add block markers to source if requested
        markers_added = []
        if self.add_markers:
            modified_source, markers_added = add_block_markers_to_source(source)

            # Write modified source back
            if markers_added:
                py_file.write_text(modified_source, encoding='utf-8')
                source = modified_source
                print(f"    Added {len(markers_added)} block markers")

        # Parse AST
        tree = ast.parse(source, filename=str(py_file))

        # Extract tags from Python file docstring
        source_tags = self._extract_python_tags(source)

        # Extract all objects
        objects = self._extract_objects(tree, source)

        # Create directory for this file's AST nodes
        rel_path = py_file.relative_to(self.code_dir)
        ast_dir = self.ast_cache_dir / "code" / rel_path.with_suffix('')
        ast_dir.mkdir(parents=True, exist_ok=True)

        # Generate one .ast.md file per object
        ast_files_created = []
        for obj in objects:
            ast_file = ast_dir / f"{obj['name']}.ast.md"
            markdown = self._generate_object_markdown(py_file, obj, objects, source_tags)

            with open(ast_file, 'w', encoding='utf-8') as f:
                f.write(markdown)

            ast_files_created.append(str(ast_file.relative_to(self.root_dir)))

        return {
            "source_hash": f"sha256:{original_hash[:16]}...",
            "ast_dir": str(ast_dir.relative_to(self.root_dir)),
            "generated_at": datetime.now().isoformat(),
            "objects_count": len(objects),
            "ast_files": ast_files_created,
            "markers_added": markers_added
        }

    def _extract_objects(self, tree: ast.AST, source: str) -> List[Dict[str, Any]]:
        """Extract all objects (functions, classes, methods, constants) from AST."""
        objects = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Determine if it's a method or function
                parent_class = None
                for parent in ast.walk(tree):
                    if isinstance(parent, ast.ClassDef):
                        if node in parent.body:
                            parent_class = parent.name
                            break

                obj = self._extract_function(node, parent_class, source)
                objects.append(obj)

            elif isinstance(node, ast.ClassDef):
                obj = self._extract_class(node, source)
                objects.append(obj)

            elif isinstance(node, ast.Assign):
                # Module-level constants
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if name.isupper() and len(name) > 1:
                            obj = self._extract_constant(node, name, source)
                            objects.append(obj)

        return objects

    def _extract_function(self, node: ast.FunctionDef, parent_class: Optional[str],
                         source: str) -> Dict[str, Any]:
        """Extract function/method information."""
        # Determine full name and marker
        if parent_class:
            full_name = f"{parent_class}.{node.name}"
            marker = f"{parent_class}-{node.name}"
            obj_type = "method"
        else:
            full_name = node.name
            marker = node.name
            obj_type = "function"

        # Extract docstring
        docstring = ast.get_docstring(node) or ""

        # Extract signature
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)

        returns = ast.unparse(node.returns) if node.returns else None

        # Check if schematic
        is_schematic = self._is_schematic(node, docstring)

        # Extract wikilinks
        wikilinks = self._extract_wikilinks(docstring)

        # Extract function calls (what this function calls)
        calls = self._extract_function_calls(node)

        return {
            "name": full_name,
            "marker": marker,
            "type": obj_type,
            "parent_class": parent_class,
            "signature": f"{node.name}({', '.join(args)})",
            "returns": returns,
            "docstring": docstring,
            "is_schematic": is_schematic,
            "wikilinks": wikilinks,
            "calls": calls,
            "lineno": node.lineno,
            "end_lineno": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
        }

    def _extract_class(self, node: ast.ClassDef, source: str) -> Dict[str, Any]:
        """Extract class information."""
        docstring = ast.get_docstring(node) or ""
        wikilinks = self._extract_wikilinks(docstring)

        # Extract method names
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)

        # Extract base classes
        bases = [ast.unparse(base) for base in node.bases]

        return {
            "name": node.name,
            "marker": node.name,
            "type": "class",
            "parent_class": None,
            "docstring": docstring,
            "wikilinks": wikilinks,
            "methods": methods,
            "bases": bases,
            "lineno": node.lineno,
            "end_lineno": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
        }

    def _extract_constant(self, node: ast.Assign, name: str, source: str) -> Dict[str, Any]:
        """Extract module-level constant information."""
        # Get value as string
        value_str = ast.unparse(node.value) if hasattr(node, 'value') else ""

        return {
            "name": name,
            "marker": name,
            "type": "constant",
            "parent_class": None,
            "value": value_str[:100],  # Truncate long values
            "lineno": node.lineno,
            "end_lineno": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
        }

    def _extract_wikilinks(self, text: str) -> List[str]:
        """Extract all wikilinks from text."""
        pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        return re.findall(pattern, text)

    def _is_schematic(self, node: ast.FunctionDef, docstring: str) -> bool:
        """Determine if function is a schematic."""
        if "Status: SCHEMATIC" in docstring or "## Behavior" in docstring:
            return True

        # Check if body is just raise NotImplementedError or pass
        if len(node.body) <= 2:
            for stmt in node.body:
                if isinstance(stmt, ast.Raise):
                    if isinstance(stmt.exc, ast.Call):
                        if isinstance(stmt.exc.func, ast.Name):
                            if stmt.exc.func.id == "NotImplementedError":
                                return True
                elif isinstance(stmt, ast.Pass):
                    return True

        return False

    def _extract_python_tags(self, source: str) -> List[str]:
        """Extract inheritable tags from Python source file docstring.

        Python docstrings should have two tag lines:
        - **File Tags**: #type/code-file (only for the .py file)
        - **Inheritable Tags**: #domain/* #layer/* (for AST nodes)

        Returns ONLY the inheritable tags (without # prefix).
        """
        # Extract module docstring (first triple-quoted string)
        match = re.match(r'^\s*"""(.*?)"""\s*\n', source, re.DOTALL)
        if not match:
            return []

        docstring = match.group(1)

        # Look for "Inheritable Tags:" line specifically
        inheritable_match = re.search(r'\*\*Inheritable Tags\*\*:\s*([^\n]+)', docstring)
        if inheritable_match:
            tag_line = inheritable_match.group(1)
            # Extract hashtags from this line only (allow dots for file extensions)
            tags = re.findall(r'#([\w/.-]+)', tag_line)
            return tags

        # Fallback: if no explicit "Inheritable Tags:" line, extract all tags and filter
        all_tags = re.findall(r'#([\w/.-]+)', docstring)
        inheritable_tags = [
            tag for tag in all_tags
            if not tag.startswith('type/')
        ]
        return inheritable_tags

    def _extract_function_calls(self, node: ast.FunctionDef) -> List[str]:
        """Extract names of functions called within this function."""
        calls = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    # Handle obj.method() calls
                    calls.append(f"{ast.unparse(child.func.value)}.{child.func.attr}")

        return list(set(calls))  # Remove duplicates

    def _extract_source_lines(self, py_file: Path, start_line: int, end_line: int) -> str:
        """Extract specific lines from source file with line numbers."""
        source_lines = py_file.read_text(encoding='utf-8').splitlines()

        # Extract the relevant lines (convert to 0-indexed)
        extracted = []
        for i in range(start_line - 1, min(end_line, len(source_lines))):
            line_num = i + 1
            line_content = source_lines[i]
            extracted.append(f"{line_num:4d} | {line_content}")

        return '\n'.join(extracted)

    def _generate_object_markdown(self, py_file: Path, obj: Dict[str, Any],
                                  all_objects: List[Dict[str, Any]],
                                  source_tags: List[str]) -> str:
        """Generate Markdown for a single Python object."""
        rel_path = py_file.relative_to(self.code_dir)

        # Link to source using block reference
        source_link = f"[[../../../code/{rel_path}#^{obj['marker']}|Source]]"

        # Extract source code with line numbers
        source_code = self._extract_source_lines(
            py_file,
            obj['lineno'],
            obj.get('end_lineno', obj['lineno'])
        )

        # Determine tags
        tags = ["type/ast-node", f"ast-type/{obj['type']}"]
        if obj.get('is_schematic'):
            tags.append("status/schematic")

        # Add inherited tags from source file
        tags.extend(source_tags)

        # Build frontmatter with YAML list format for tags
        lines = [
            "---",
            "tags:",
        ]
        for tag in tags:
            lines.append(f"  - {tag}")
        # Separate AST-specific tags from inherited tags
        ast_tags = ["type/ast-node", f"ast-type/{obj['type']}"]
        if obj.get('is_schematic'):
            ast_tags.append("status/schematic")

        # Format line number range
        line_range = f"{obj['lineno']}"
        if obj.get('end_lineno') and obj['end_lineno'] != obj['lineno']:
            line_range = f"{obj['lineno']}-{obj['end_lineno']}"

        lines.extend([
            f"source_file: ../../../code/{rel_path}",
            f"block_marker: ^{obj['marker']}",
            f"object_type: {obj['type']}",
            f"line_start: {obj['lineno']}",
            f"line_end: {obj.get('end_lineno', obj['lineno'])}",
            "---",
            "",
            "> [!WARNING] Generated Code - Do Not Edit",
            f"> This file is auto-generated. Please edit the source code block in [[../../../code/{rel_path}#^{obj['marker']}]] and run `uv run update.py` to regenerate.",
            "",
            f"# {obj['name']}",
            "",
            f"**Source**: {source_link} (lines {line_range})",
            f"**Type**: {obj['type']}",
            ""
        ])

        # Brief tag inheritance note (no links to avoid graph clutter)
        if source_tags:
            lines.extend([
                f"**Tags**: {len(source_tags)} inherited from module + {len(ast_tags)} AST-specific",
                ""
            ])
        else:
            lines.append("")

        # Type-specific information
        if obj['type'] == 'function' or obj['type'] == 'method':
            lines.append(f"**Signature**: `{obj['signature']}`")
            if obj.get('returns'):
                lines.append(f"**Returns**: `{obj['returns']}`")
            if obj.get('is_schematic'):
                lines.append(f"**Status**: SCHEMATIC (not yet implemented)")
            lines.append("")

            # Docstring
            if obj.get('docstring'):
                lines.append("## Documentation")
                lines.append("")
                lines.append(obj['docstring'])
                lines.append("")

            # Source code with line numbers
            lines.append("## Source Code")
            lines.append("")
            lines.append(f"```python")
            lines.append(source_code)
            lines.append("```")
            lines.append("")

            # Function calls
            if obj.get('calls'):
                lines.append("## Calls")
                lines.append("")
                lines.append("This function calls:")
                for call in obj['calls']:
                    # Try to create link to AST node if it exists
                    link_created = False

                    # Normalize the call name (handle self.method -> ClassName.method)
                    call_name = call.replace('self.', '')

                    for other_obj in all_objects:
                        other_name = other_obj['name']

                        # Match full name or method name
                        if (other_name == call_name or
                            other_name.endswith(f".{call_name}") or
                            (call_name.startswith('_') and other_name.endswith(call_name))):

                            # Create relative link to other AST file
                            lines.append(f"- [[{other_name}.ast.md|{call}]] (internal)")
                            link_created = True
                            break

                    if not link_created:
                        lines.append(f"- `{call}` (external or built-in)")
                lines.append("")

        elif obj['type'] == 'class':
            if obj.get('bases'):
                lines.append(f"**Inherits**: {', '.join(obj['bases'])}")
                lines.append("")

            # Docstring
            if obj.get('docstring'):
                lines.append("## Documentation")
                lines.append("")
                lines.append(obj['docstring'])
                lines.append("")

            # Source code with line numbers
            lines.append("## Source Code")
            lines.append("")
            lines.append(f"```python")
            lines.append(source_code)
            lines.append("```")
            lines.append("")

            # Methods
            if obj.get('methods'):
                lines.append("## Methods")
                lines.append("")
                for method in obj['methods']:
                    method_link = f"[[{obj['name']}.{method}.ast.md|{method}]]"
                    lines.append(f"- {method_link}")
                lines.append("")

        elif obj['type'] == 'constant':
            lines.append(f"**Value**: `{obj.get('value', 'N/A')}`")
            lines.append("")

            # Source code with line numbers
            lines.append("## Source Code")
            lines.append("")
            lines.append(f"```python")
            lines.append(source_code)
            lines.append("```")
            lines.append("")

        # Wikilinks in docstring
        if obj.get('wikilinks'):
            lines.append("## Documentation References")
            lines.append("")
            lines.append("Links to conceptual documentation:")
            for link in obj['wikilinks']:
                # All wikilinks should be clickable, no backticks
                lines.append(f"- [[{link}]]")
            lines.append("")

        return '\n'.join(lines)


def main():
    import sys

    # Script is in maintenance_scripts/, root is parent
    root_dir = Path(__file__).parent.parent

    # Parse arguments
    clean = "--clean" in sys.argv
    no_markers = "--no-markers" in sys.argv

    generator = ASTGenerator(root_dir, add_markers=not no_markers)

    print("=" * 60)
    print("AST Cache Generator v2.0")
    print("=" * 60)
    print()
    print(f"Root directory: {root_dir}")
    print(f"Code directory: {generator.code_dir}")
    print(f"AST cache directory: {generator.ast_cache_dir}")
    print(f"Add block markers: {not no_markers}")
    print()

    generator.generate_all(clean=clean)

    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
