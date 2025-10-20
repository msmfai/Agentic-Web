#!/usr/bin/env python3
"""
# Tag Index Generator

**Tags**: #type/code-file #domain/automation #layer/infrastructure #category/indexing

## Purpose
Generate Tag Index for Obsidian Knowledge Graph

This script scans all files in the repository and generates:
1. repository-map.md - High-level project state snapshot
2. tag-index.md - Complete exhaustive tag inventory

Both files are auto-generated and should not be edited manually.

Usage:
    python generate_tags.py
    uv run generate_tags.py
"""

import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class TagScanner:
    """Scans repository and collects tag data from all files."""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

        # Data structures
        self.tags_to_files: Dict[str, List[Path]] = defaultdict(list)
        self.file_counts: Dict[str, int] = defaultdict(int)
        self.all_tags: Set[str] = set()

        # Directories to skip
        self.skip_dirs = {'.git', '.obsidian', '__pycache__', 'node_modules', '.venv', 'venv', 'whiteboard'}

    def parse_yaml_frontmatter(self, content: str) -> List[str]:
        """Extract tags from YAML frontmatter."""
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return []

        yaml_content = match.group(1)

        # Try inline array format first: tags: [tag1, tag2, tag3]
        tags_match_inline = re.search(r'tags:\s*\[(.*?)\]', yaml_content)
        if tags_match_inline:
            tags_str = tags_match_inline.group(1)
            return [t.strip().strip('"').strip("'") for t in tags_str.split(',')]

        # Try YAML list format: tags:\n  - tag1\n  - tag2
        tags_match_list = re.search(r'tags:\s*\n((?:\s+-\s+.+\n?)+)', yaml_content)
        if tags_match_list:
            tags_str = tags_match_list.group(1)
            return [line.strip().lstrip('-').strip() for line in tags_str.strip().split('\n')]

        return []

    def parse_python_docstring_tags(self, content: str) -> List[str]:
        """Extract tags from Python custom frontmatter format."""
        # Extract module docstring
        match = re.match(r'^\s*"""(.*?)"""\s*\n', content, re.DOTALL)
        if not match:
            return []

        docstring = match.group(1)

        # Extract inline tags: **Tags**: #tag1 #tag2 #tag3
        tags_match = re.search(r'\*\*Tags\*\*:\s*(.+)$', docstring, re.MULTILINE)
        if not tags_match:
            return []

        tags_line = tags_match.group(1)
        # Extract all #hashtags (without the # prefix)
        tags = re.findall(r'#([\w/-]+)', tags_line)
        return tags

    def should_skip_path(self, path: Path) -> bool:
        """Check if a path should be skipped."""
        # Skip directories in skip list
        for part in path.parts:
            if part in self.skip_dirs:
                return True

        # Skip auto-generated tag index files
        if path.name in ['repository-map.md', 'tag-index.md']:
            return True

        return False

    def scan_file(self, filepath: Path) -> None:
        """Scan a single file for tags."""
        if self.should_skip_path(filepath):
            return

        try:
            content = filepath.read_text(encoding='utf-8')
            tags = []

            # Determine file type and extract tags
            if filepath.suffix == '.py':
                tags = self.parse_python_docstring_tags(content)
                self.file_counts['python'] += 1
            elif filepath.suffix == '.md':
                tags = self.parse_yaml_frontmatter(content)

                # Categorize markdown files by type tag
                if 'type/concept' in tags:
                    self.file_counts['concept'] += 1
                elif 'type/pattern' in tags:
                    self.file_counts['pattern'] += 1
                elif 'type/index' in tags:
                    self.file_counts['index'] += 1
                elif 'type/ast-node' in tags:
                    self.file_counts['ast-cache'] += 1
                elif 'type/case-study' in tags:
                    self.file_counts['case-study'] += 1
                else:
                    self.file_counts['other-md'] += 1

            # Store tags
            if tags:
                for tag in tags:
                    self.tags_to_files[tag].append(filepath)
                    self.all_tags.add(tag)

        except Exception as e:
            print(f"  WARNING: Could not parse {filepath.relative_to(self.root_dir)}: {e}")

    def scan_repository(self) -> None:
        """Scan entire repository for tags."""
        print("Scanning repository for tags...")

        # Recursively scan all files
        for filepath in self.root_dir.rglob('*'):
            if filepath.is_file():
                self.scan_file(filepath)

        print(f"Found {len(self.all_tags)} unique tags across {sum(self.file_counts.values())} files")

    def group_tags_by_hierarchy(self) -> Dict[str, List[str]]:
        """Group tags by their hierarchy prefix."""
        grouped: Dict[str, List[str]] = defaultdict(list)

        for tag in sorted(self.all_tags):
            if '/' in tag:
                prefix = tag.split('/', 1)[0]
                grouped[prefix].append(tag)
            else:
                grouped['other'].append(tag)

        return dict(grouped)

    def get_file_link(self, filepath: Path) -> str:
        """Generate Obsidian wikilink for a file (from index/ perspective)."""
        rel_path = filepath.relative_to(self.root_dir)
        obsidian_dir = self.root_dir / "obsidian"

        # Determine the directory the file is in
        try:
            # Files in obsidian/ - use relative path from index/
            if filepath.parent == obsidian_dir:
                return f"[[../obsidian/{filepath.stem}|{filepath.name}]]"

            # Files elsewhere - use relative path from index/
            # Convert to posix for consistent wikilinks
            rel_from_index = Path("..") / rel_path
            link_path = rel_from_index.as_posix()

            # Use stem for .ast.md files, otherwise use name
            display = filepath.stem if filepath.suffix == '.md' and '.ast' in filepath.stem else filepath.name

            return f"[[{link_path}|{display}]]"

        except ValueError:
            # Fallback for files outside root
            return f"`{rel_path}`"

    def generate_repository_map(self) -> str:
        """Generate repository-map.md content."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        grouped_tags = self.group_tags_by_hierarchy()

        lines = [
            "---",
            "tags:",
            "  - type/index",
            "  - purpose/project-state",
            "  - auto-generated",
            "---",
            "",
            "# Repository Map",
            "",
            "**Auto-generated - do not edit manually**",
            "",
            f"**Last Updated**: {now}",
            "",
            "## Current Scale",
            "",
            f"- Python files: {self.file_counts.get('python', 0)}",
            f"- Concept docs: {self.file_counts.get('concept', 0)}",
            f"- Pattern docs: {self.file_counts.get('pattern', 0)}",
            f"- Case studies: {self.file_counts.get('case-study', 0)}",
            f"- Index files: {self.file_counts.get('index', 0)}",
            f"- AST cache nodes: {self.file_counts.get('ast-cache', 0)}",
            f"- Other markdown: {self.file_counts.get('other-md', 0)}",
            "",
        ]

        # Active Domains
        if 'domain' in grouped_tags:
            lines.extend([
                "## Active Domains",
                "",
            ])
            for tag in sorted(grouped_tags['domain']):
                file_count = len(self.tags_to_files[tag])
                # Get first few files as examples
                example_files = self.tags_to_files[tag][:3]
                example_links = ', '.join(self.get_file_link(f) for f in example_files)
                more_text = f" (+{file_count - 3} more)" if file_count > 3 else ""

                lines.append(f"- `#{tag}` ({file_count} files): {example_links}{more_text}")
            lines.append("")

        # Active Layers
        if 'layer' in grouped_tags:
            lines.extend([
                "## Active Layers",
                "",
            ])
            for tag in sorted(grouped_tags['layer']):
                file_count = len(self.tags_to_files[tag])
                example_files = self.tags_to_files[tag][:3]
                example_links = ', '.join(self.get_file_link(f) for f in example_files)
                more_text = f" (+{file_count - 3} more)" if file_count > 3 else ""

                lines.append(f"- `#{tag}` ({file_count} files): {example_links}{more_text}")
            lines.append("")

        # Implemented Patterns
        if 'pattern' in grouped_tags:
            lines.extend([
                "## Implemented Patterns",
                "",
            ])
            for tag in sorted(grouped_tags['pattern']):
                file_count = len(self.tags_to_files[tag])
                example_files = self.tags_to_files[tag][:3]
                example_links = ', '.join(self.get_file_link(f) for f in example_files)
                more_text = f" (+{file_count - 3} more)" if file_count > 3 else ""

                lines.append(f"- `#{tag}` ({file_count} files): {example_links}{more_text}")
            lines.append("")

        # Reference to complete index
        lines.extend([
            "## Complete Tag Inventory",
            "",
            "See [[tag-index|Complete Tag Index]] for exhaustive list of all tags.",
            "",
            "**Note**: The tag index file contains all repository tags in its frontmatter, making it part of the graph through tags rather than wikilinks.",
            "",
        ])

        return '\n'.join(lines)

    def generate_tag_index(self) -> str:
        """Generate tag-index.md content."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        grouped_tags = self.group_tags_by_hierarchy()

        # Build the frontmatter with ALL tags currently in use
        # This makes the file part of the graph through tags, not wikilinks
        frontmatter_tags = ["  - type/index", "  - purpose/tag-inventory", "  - auto-generated"]
        for tag in sorted(self.all_tags):
            frontmatter_tags.append(f"  - {tag}")

        lines = [
            "---",
            "tags:",
        ]
        lines.extend(frontmatter_tags)
        lines.extend([
            "---",
            "",
            "# Complete Tag Index",
            "",
            "**Auto-generated - do not edit manually**",
            "",
            f"**Last Updated**: {now}",
            "",
            "This file lists every tag currently in use across the repository.",
            "",
            "## Summary",
            "",
            f"- Total unique tags: {len(self.all_tags)}",
            f"- Total files: {sum(self.file_counts.values())}",
            "",
        ])

        # Generate sections for each tag hierarchy - just list tags with counts, no file links
        hierarchy_order = ['type', 'domain', 'layer', 'pattern', 'category', 'purpose', 'ast-type', 'status', 'severity', 'other']

        for prefix in hierarchy_order:
            if prefix not in grouped_tags:
                continue

            # Capitalize prefix for section title
            section_title = f"{prefix.title()} Tags" if prefix != 'other' else "Other Tags"
            lines.extend([
                f"## {section_title}",
                "",
            ])

            for tag in sorted(grouped_tags[prefix]):
                file_count = len(self.tags_to_files[tag])
                lines.append(f"- `#{tag}` ({file_count} files)")

            lines.append("")

        return '\n'.join(lines)

    def write_generated_files(self) -> None:
        """Write repository-map.md and tag-index.md to index/ directory."""
        index_dir = self.root_dir / "index"
        index_dir.mkdir(exist_ok=True)

        # Generate and write repository map
        repo_map_path = index_dir / "repository-map.md"
        repo_map_content = self.generate_repository_map()
        repo_map_path.write_text(repo_map_content, encoding='utf-8')
        print(f"Generated: {repo_map_path.relative_to(self.root_dir)}")

        # Generate and write tag index
        tag_index_path = index_dir / "tag-index.md"
        tag_index_content = self.generate_tag_index()
        tag_index_path.write_text(tag_index_content, encoding='utf-8')
        print(f"Generated: {tag_index_path.relative_to(self.root_dir)}")


def main():
    root_dir = Path(__file__).parent

    print("=" * 60)
    print("Tag Index Generator")
    print("=" * 60)
    print()
    print(f"Root directory: {root_dir}")
    print()

    scanner = TagScanner(root_dir)
    scanner.scan_repository()
    print()
    scanner.write_generated_files()

    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
