#!/usr/bin/env python3
"""
# Repository Health Janitor

**Tags**: #type/code-file #domain/automation #layer/infrastructure #category/validation

## Purpose
Validate and automatically fix issues in the Obsidian knowledge graph repository.

Checks:
- All files have required YAML frontmatter tags
- Python file docstring schema compliance
- Markdown files are in correct folders

Usage:
    python janitor.py              # Check for issues
    python janitor.py --fix        # Auto-fix issues with confirmation
    python janitor.py --fix --yes  # Auto-fix without confirmation
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass


@dataclass
class Issue:
    """Represents a validation issue found in a file."""
    filepath: Path
    severity: str  # 'error' or 'warning'
    message: str
    fix_available: bool = False
    fix_description: str = ""
    auto_fix_fn: Optional[callable] = None


class RepositoryJanitor:
    """Validates and fixes repository structure and content."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.issues: List[Issue] = []
        # Track all block markers across repository for reference validation
        self.block_markers: Dict[str, Tuple[Path, int]] = {}  # marker -> (file, lineno)
        self.block_marker_references: List[Tuple[Path, int, str]] = []  # (file, line, marker)

        # Track all wikilinks for link restriction validation
        self.file_links: Dict[Path, List[Tuple[Path, int]]] = {}  # source -> [(target, lineno), ...]

        # Load schema from schema.yaml (scaffold base types)
        self.schema = self._load_schema()

        # Load project-specific tag rules from project_config/tag_rules.yaml
        self.project_tag_rules = self._load_project_tag_rules()

    def _load_schema(self) -> Dict[str, Any]:
        """Load schema from schema.yaml file."""
        schema_file = self.vault_path / "schema.yaml"
        if not schema_file.exists():
            print(f"WARNING: schema.yaml not found at {schema_file}")
            return {}

        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                # YAML file has multiple documents separated by ---
                # We need to load all of them
                schema_docs = list(yaml.safe_load_all(f))

                # Combine all documents into single dict
                combined = {}
                for doc in schema_docs:
                    if doc:
                        combined.update(doc)

                return combined
        except Exception as e:
            print(f"ERROR: Failed to load schema.yaml: {e}")
            return {}

    def _load_project_tag_rules(self) -> Dict[str, Any]:
        """Load user-defined tag rules from project_config/tag_rules.yaml"""
        rules_file = self.vault_path / "project_config" / "tag_rules.yaml"

        if not rules_file.exists():
            # No project tag rules is fine - it's optional
            return {}

        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                rules = yaml.safe_load(f)
                return rules or {}
        except Exception as e:
            print(f"WARNING: Failed to load project tag rules: {e}")
            return {}

    # ==================== SCHEMA DEFINITIONS ====================

    REQUIRED_TAGS = {
        # Python code files must have these tags
        'code-file': {
            'required': ['type/code-file'],
            'recommended': ['domain/*', 'layer/*'],
            'optional': ['pattern/*']
        },
        # Markdown concept files
        'concept': {
            'required': ['type/concept'],
            'recommended': ['domain/*', 'layer/*'],
            'optional': []
        },
        # Markdown pattern files
        'pattern': {
            'required': ['type/pattern'],
            'recommended': ['category/*'],
            'optional': []
        },
        # Index files
        'index': {
            'required': ['type/index'],
            'recommended': [],
            'optional': []
        }
    }

    PYTHON_DOCSTRING_SCHEMA = """
\"\"\"
# Module Name

**Tags**: #type/code-file #domain/* #layer/*

## Purpose
Brief description

## Related Documentation
- Concept: [[concept-file|Display]]
- Pattern: [[pattern-file|Display]]

## Dependencies
- [[other-file.py|Display]]
\"\"\"
"""

    # ==================== PARSING UTILITIES ====================

    def parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract YAML frontmatter and return (frontmatter_dict, remaining_content)."""
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not match:
            return None, content

        yaml_content = match.group(1)
        remaining = match.group(2)

        # Use yaml.safe_load to parse all YAML properties properly
        try:
            frontmatter = yaml.safe_load(yaml_content) or {}
        except Exception:
            # Fall back to old regex-based parsing if YAML parsing fails
            frontmatter = {}

        # Track tag format for validation
        yaml_content_check = yaml_content.replace('\n', ' ')
        if 'tags: [' in yaml_content_check or 'tags:[' in yaml_content_check:
            frontmatter['_tag_format'] = 'inline'
        elif 'tags:\n' in yaml_content or 'tags: \n' in yaml_content:
            frontmatter['_tag_format'] = 'yaml-list'

        return frontmatter, remaining

    def extract_python_docstring(self, content: str) -> Optional[str]:
        """Extract the module-level docstring from Python file."""
        # Match triple-quoted docstring at start of file
        match = re.match(r'^\s*"""(.*?)"""\s*\n', content, re.DOTALL)
        if match:
            return match.group(1)
        return None

    def parse_python_custom_frontmatter(self, docstring: str) -> Tuple[Optional[Dict], str]:
        """Parse custom frontmatter format for Python files.

        Expected format:
        # Module Name

        **Tags**: #tag1 #tag2 #tag3

        ## Purpose
        Description...

        Returns:
            (frontmatter_dict, remaining_content)
        """
        frontmatter = {}

        # Extract H1 module name
        h1_match = re.search(r'^#\s+(.+)$', docstring, re.MULTILINE)
        if h1_match:
            frontmatter['module_name'] = h1_match.group(1).strip()

        # Extract inline tags - supports both old and new formats:
        # Old: **Tags**: #tag1 #tag2 #tag3
        # New: **File Tags**: #tag1
        #      **Inheritable Tags**: #tag2 #tag3

        all_tags = []

        # Try new format first (File Tags + Inheritable Tags)
        file_tags_match = re.search(r'\*\*File Tags\*\*:\s*(.+)$', docstring, re.MULTILINE)
        inheritable_tags_match = re.search(r'\*\*Inheritable Tags\*\*:\s*(.+)$', docstring, re.MULTILINE)

        if file_tags_match or inheritable_tags_match:
            # New format detected
            if file_tags_match:
                file_tags = re.findall(r'#([\w/.-]+)', file_tags_match.group(1))
                all_tags.extend(file_tags)
            if inheritable_tags_match:
                inheritable_tags = re.findall(r'#([\w/.-]+)', inheritable_tags_match.group(1))
                all_tags.extend(inheritable_tags)
            frontmatter['_tag_format'] = 'split-tags'
        else:
            # Fallback to old format (**Tags**: #tag1 #tag2 #tag3)
            tags_match = re.search(r'\*\*Tags\*\*:\s*(.+)$', docstring, re.MULTILINE)
            if tags_match:
                tags_line = tags_match.group(1)
                all_tags = re.findall(r'#([\w/.-]+)', tags_line)
                frontmatter['_tag_format'] = 'inline-hashtags'

        if all_tags:
            frontmatter['tags'] = all_tags

        # Check for required sections
        has_purpose = bool(re.search(r'^##\s+Purpose', docstring, re.MULTILINE))
        frontmatter['has_purpose'] = has_purpose

        return frontmatter, docstring

    def validate_block_markers(self, filepath: Path, content: str) -> None:
        """Validate Obsidian block reference markers in Python file.

        Checks that:
        - Every function/class/method/constant has a block marker (# ^name)
        - Block marker naming is consistent with object name
        - No duplicate block IDs in same file
        - Collects all markers for cross-reference validation
        """
        import ast

        try:
            tree = ast.parse(content, filename=str(filepath))
        except SyntaxError as e:
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message=f"Syntax error in Python file: {e}",
                fix_available=False
            ))
            return

        lines = content.split('\n')

        # Extract all block markers from file (for duplicate detection and registry)
        file_markers = {}
        for lineno, line in enumerate(lines, 1):
            marker_match = re.search(r'#\s*\^(\S+)', line)
            if marker_match:
                marker = marker_match.group(1)

                # Check for duplicates within this file
                if marker in file_markers:
                    self.issues.append(Issue(
                        filepath=filepath,
                        severity='error',
                        message=f"Duplicate block marker ^{marker} in same file (lines {file_markers[marker]} and {lineno})",
                        fix_available=False
                    ))
                else:
                    file_markers[marker] = lineno

                    # Check for duplicates across entire repository
                    # CHANGED: Duplicate markers across files are now allowed (e.g., PLUGIN_OPERATIONS in multiple plugins)
                    # Only register the FIRST occurrence for reference validation
                    if marker not in self.block_markers:
                        # Register this marker globally
                        self.block_markers[marker] = (filepath, lineno)

        # Track which objects we've found to detect orphaned markers
        expected_markers = set()

        # Check all functions, classes, methods, and constants have markers
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Determine expected marker name
                parent_class = None
                for parent in ast.walk(tree):
                    if isinstance(parent, ast.ClassDef):
                        if node in parent.body:
                            parent_class = parent.name
                            break

                if parent_class:
                    expected_marker = f"{parent_class}-{node.name}"
                    obj_desc = f"method {parent_class}.{node.name}"
                else:
                    expected_marker = node.name
                    obj_desc = f"function {node.name}"

                expected_markers.add(expected_marker)

                # Check if marker exists on this line
                if node.lineno <= len(lines):
                    line = lines[node.lineno - 1]
                    if f"# ^{expected_marker}" not in line:
                        self.issues.append(Issue(
                            filepath=filepath,
                            severity='error',
                            message=f"Missing block marker for {obj_desc} at line {node.lineno}. Expected: # ^{expected_marker}",
                            fix_available=False
                        ))
                    else:
                        # Verify the marker name is exactly correct
                        marker_match = re.search(r'#\s*\^(\S+)', line)
                        if marker_match:
                            actual_marker = marker_match.group(1)
                            if actual_marker != expected_marker:
                                self.issues.append(Issue(
                                    filepath=filepath,
                                    severity='error',
                                    message=f"Incorrect block marker for {obj_desc} at line {node.lineno}. Found ^{actual_marker}, expected ^{expected_marker}",
                                    fix_available=False
                                ))

            elif isinstance(node, ast.ClassDef):
                expected_marker = node.name
                obj_desc = f"class {node.name}"
                expected_markers.add(expected_marker)

                # Check if marker exists on this line
                if node.lineno <= len(lines):
                    line = lines[node.lineno - 1]
                    if f"# ^{expected_marker}" not in line:
                        self.issues.append(Issue(
                            filepath=filepath,
                            severity='error',
                            message=f"Missing block marker for {obj_desc} at line {node.lineno}. Expected: # ^{expected_marker}",
                            fix_available=False
                        ))
                    else:
                        # Verify the marker name is exactly correct
                        marker_match = re.search(r'#\s*\^(\S+)', line)
                        if marker_match:
                            actual_marker = marker_match.group(1)
                            if actual_marker != expected_marker:
                                self.issues.append(Issue(
                                    filepath=filepath,
                                    severity='error',
                                    message=f"Incorrect block marker for {obj_desc} at line {node.lineno}. Found ^{actual_marker}, expected ^{expected_marker}",
                                    fix_available=False
                                ))

            elif isinstance(node, ast.Assign):
                # Check module-level constants (ALL_CAPS)
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if name.isupper() and len(name) > 1:
                            expected_marker = name
                            obj_desc = f"constant {name}"
                            expected_markers.add(expected_marker)

                            # Check if marker exists on this line
                            if node.lineno <= len(lines):
                                line = lines[node.lineno - 1]
                                if f"# ^{expected_marker}" not in line:
                                    self.issues.append(Issue(
                                        filepath=filepath,
                                        severity='warning',
                                        message=f"Missing block marker for {obj_desc} at line {node.lineno}. Expected: # ^{expected_marker}",
                                        fix_available=False
                                    ))

        # Check for orphaned markers (markers that don't correspond to any object)
        for marker in file_markers.keys():
            if marker not in expected_markers:
                self.issues.append(Issue(
                    filepath=filepath,
                    severity='warning',
                    message=f"Orphaned block marker ^{marker} at line {file_markers[marker]} does not correspond to any function/class/constant",
                    fix_available=False
                ))

    # ==================== VALIDATION FUNCTIONS ====================

    def validate_python_file(self, filepath: Path) -> None:
        """Validate a Python code file."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message=f"Could not read file: {e}",
                fix_available=False
            ))
            return

        # Extract docstring
        docstring = self.extract_python_docstring(content)
        if not docstring:
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message="Missing module-level docstring",
                fix_available=True,
                fix_description="Add template docstring with frontmatter",
                auto_fix_fn=lambda: self.fix_add_python_docstring(filepath)
            ))
            return

        # Parse custom frontmatter from docstring (Python-specific format)
        frontmatter, _ = self.parse_python_custom_frontmatter(docstring)
        if not frontmatter:
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message="Docstring missing custom frontmatter (needs # Module Name and **Tags**: line)",
                fix_available=False
            ))
            return

        # Check for H1 module name
        if not frontmatter.get('module_name'):
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message="Docstring missing H1 module name (# Module Name)",
                fix_available=False
            ))

        # Check for Tags line (either old or new format)
        if not frontmatter.get('tags'):
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message="Docstring missing tags (need either **Tags**: OR **File Tags**:/**Inheritable Tags**: with #hashtags)",
                fix_available=False
            ))
            return

        # Check for Purpose section
        if not frontmatter.get('has_purpose'):
            self.issues.append(Issue(
                filepath=filepath,
                severity='warning',
                message="Docstring missing ## Purpose section",
                fix_available=False
            ))

        # Check required tags
        tags = set(frontmatter.get('tags', []))
        schema = self.REQUIRED_TAGS['code-file']

        for required_tag in schema['required']:
            if required_tag not in tags:
                self.issues.append(Issue(
                    filepath=filepath,
                    severity='error',
                    message=f"Missing required tag: {required_tag}",
                    fix_available=True,
                    fix_description=f"Add '{required_tag}' to tags",
                    auto_fix_fn=lambda tag=required_tag: self.fix_add_tag(filepath, tag)
                ))

        # Check recommended tags (warnings only)
        has_recommended = False
        for rec_pattern in schema['recommended']:
            if rec_pattern.endswith('/*'):
                prefix = rec_pattern[:-2]
                has_recommended = any(t.startswith(prefix + '/') for t in tags)
                if has_recommended:
                    break

        if not has_recommended and schema['recommended']:
            self.issues.append(Issue(
                filepath=filepath,
                severity='warning',
                message=f"Missing recommended tags: {', '.join(schema['recommended'])}",
                fix_available=False
            ))

        # Validate block markers
        self.validate_block_markers(filepath, content)

    def validate_markdown_file(self, filepath: Path) -> None:
        """Validate a markdown documentation file."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message=f"Could not read file: {e}",
                fix_available=False
            ))
            return

        # Parse frontmatter
        frontmatter, _ = self.parse_frontmatter(content)
        if not frontmatter:
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message="Missing YAML frontmatter",
                fix_available=True,
                fix_description="Add frontmatter with tags",
                auto_fix_fn=lambda: self.fix_add_markdown_frontmatter(filepath)
            ))
            return

        # Check tag format (prefer YAML list for Obsidian compatibility)
        if frontmatter.get('_tag_format') == 'inline':
            self.issues.append(Issue(
                filepath=filepath,
                severity='warning',
                message="Tags use inline array format [tag1, tag2]. Obsidian prefers YAML list format for hierarchical tags",
                fix_available=False
            ))

        # Determine file type from tags
        tags = set(frontmatter.get('tags', []))
        file_type = None
        for tag in tags:
            if tag.startswith('type/'):
                file_type = tag.split('/', 1)[1]
                break

        if not file_type:
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message="Missing type/* tag (e.g., type/concept, type/pattern, type/index)",
                fix_available=False
            ))
            return

        # Validate against schema
        if file_type in self.REQUIRED_TAGS:
            schema = self.REQUIRED_TAGS[file_type]
            for required_tag in schema['required']:
                if required_tag not in tags:
                    self.issues.append(Issue(
                        filepath=filepath,
                        severity='error',
                        message=f"Missing required tag: {required_tag}",
                        fix_available=True,
                        fix_description=f"Add '{required_tag}' to tags",
                        auto_fix_fn=lambda tag=required_tag: self.fix_add_tag(filepath, tag)
                    ))

        # NEW: Validate project-specific tag property requirements
        self.validate_tag_properties(filepath, frontmatter)

    def validate_tag_properties(self, filepath: Path, frontmatter: dict) -> None:
        """Validate that files with project-defined tags have required properties."""
        tags = set(frontmatter.get('tags', []))

        # Skip project tag validation for auto-generated files
        # These files may have many tags for graph purposes but aren't "real" instances of those tags
        if 'auto-generated' in tags:
            return

        # Check each project-defined tag rule
        for rule_name, rule_config in self.project_tag_rules.items():
            required_tag = rule_config.get('tag')

            if required_tag in tags:
                enforcement = rule_config.get('enforcement', 'warning')

                # Validate required properties exist
                for prop in rule_config.get('required_properties', []):
                    if prop not in frontmatter:
                        self.issues.append(Issue(
                            filepath=filepath,
                            severity=enforcement,
                            message=f"Tag '{required_tag}' requires property '{prop}' in frontmatter",
                            fix_available=True,
                            fix_description=f"Add '{prop}: FIXME' to frontmatter",
                            auto_fix_fn=lambda p=prop: self.fix_add_property(filepath, p, 'FIXME')
                        ))

                # Validate property patterns (if defined)
                for prop, pattern in rule_config.get('property_patterns', {}).items():
                    if prop in frontmatter:
                        value = str(frontmatter[prop])
                        if not re.match(pattern, value):
                            self.issues.append(Issue(
                                filepath=filepath,
                                severity=enforcement,
                                message=f"Property '{prop}' value '{value}' doesn't match required pattern: {pattern}",
                                fix_available=False
                            ))

    # ==================== FIX FUNCTIONS ====================

    def fix_add_python_docstring(self, filepath: Path) -> bool:
        """Add template docstring to Python file."""
        content = filepath.read_text(encoding='utf-8')

        template = '''"""
---
tags: [type/code-file, domain/FIXME, layer/FIXME]
---

# {}

## Purpose
TODO: Brief description of what this module does.

## Related Documentation
- Concept: [[FIXME|Concept Name]]

## Dependencies
- [[FIXME.py|Dependency Name]]
"""

'''.format(filepath.stem.replace('_', ' ').title())

        new_content = template + content
        filepath.write_text(new_content, encoding='utf-8')
        return True

    def fix_add_frontmatter_to_docstring(self, filepath: Path) -> bool:
        """Add frontmatter to existing docstring."""
        content = filepath.read_text(encoding='utf-8')
        docstring = self.extract_python_docstring(content)

        if not docstring:
            return False

        # Add frontmatter at start of docstring
        frontmatter = '''---
tags: [type/code-file, domain/FIXME, layer/FIXME]
---

'''
        new_docstring = frontmatter + docstring.lstrip()

        # Replace old docstring with new one
        new_content = re.sub(
            r'^\s*"""(.*?)"""\s*\n',
            f'"""{new_docstring}"""\n',
            content,
            count=1,
            flags=re.DOTALL
        )

        filepath.write_text(new_content, encoding='utf-8')
        return True

    def fix_add_tag(self, filepath: Path, tag: str) -> bool:
        """Add a tag to file's frontmatter."""
        content = filepath.read_text(encoding='utf-8')

        # Find and update the tags line
        def add_tag_to_line(match):
            tags_content = match.group(1)
            # Parse existing tags
            existing_tags = [t.strip().strip('"').strip("'") for t in tags_content.split(',')]
            if tag not in existing_tags:
                existing_tags.append(tag)
            # Rebuild tags line
            tags_str = ', '.join(existing_tags)
            return f'tags: [{tags_str}]'

        new_content = re.sub(r'tags:\s*\[(.*?)\]', add_tag_to_line, content, count=1)
        filepath.write_text(new_content, encoding='utf-8')
        return True

    def fix_add_markdown_frontmatter(self, filepath: Path) -> bool:
        """Add frontmatter to markdown file."""
        content = filepath.read_text(encoding='utf-8')

        frontmatter = '''---
tags: [type/FIXME]
---

'''
        new_content = frontmatter + content
        filepath.write_text(new_content, encoding='utf-8')
        return True

    def fix_add_property(self, filepath: Path, property_name: str, default_value: str) -> bool:
        """Add a missing property to YAML frontmatter."""
        content = filepath.read_text(encoding='utf-8')

        if not content.startswith('---'):
            return False

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False

        fm_content = parts[1]
        body = parts[2]

        # Add property to frontmatter (YAML format)
        new_fm = fm_content.rstrip() + f"\n{property_name}: {default_value}\n"
        new_content = f"---{new_fm}---{body}"

        filepath.write_text(new_content, encoding='utf-8')
        return True

    # ==================== MAIN EXECUTION ====================

    def extract_block_marker_references(self, filepath: Path, content: str) -> None:
        """Extract all block marker references from a file.

        Looks for patterns like:
        - [[file.py#^marker|Display]]
        - [[../code/file.py#^marker]]
        """
        lines = content.split('\n')

        # Pattern to match [[file#^marker]] or [[file#^marker|display]]
        pattern = r'\[\[([^\]]+?)#\^([^\]|]+)(?:\|[^\]]+)?\]\]'

        for lineno, line in enumerate(lines, 1):
            for match in re.finditer(pattern, line):
                referenced_file = match.group(1)
                marker = match.group(2)
                self.block_marker_references.append((filepath, lineno, marker))

    def validate_all_block_marker_references(self) -> None:
        """Validate that all block marker references point to existing markers."""
        for ref_file, ref_line, marker in self.block_marker_references:
            if marker not in self.block_markers:
                self.issues.append(Issue(
                    filepath=ref_file,
                    severity='error',
                    message=f"Dead block marker reference at line {ref_line}: ^{marker} does not exist in any Python file",
                    fix_available=False
                ))

    def extract_wikilinks(self, filepath: Path, content: str) -> None:
        """Extract all wikilinks from a file and validate they point to existing files.

        Looks for patterns like:
        - [[file-name]]
        - [[file-name|Display]]
        - [[../code/file.py]]
        - [[../code/file.py|Display]]
        - [[file#^marker]]
        - [[file#^marker|Display]]
        """
        lines = content.split('\n')

        # Pattern to match [[link]] or [[link|display]]
        # Captures: [[path/to/file#section|display text]]
        pattern = r'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]'

        for lineno, line in enumerate(lines, 1):
            for match in re.finditer(pattern, line):
                link_path = match.group(1).strip()

                # Resolve the link path relative to the source file
                target_path = self._resolve_wikilink(filepath, link_path)

                if target_path and not target_path.exists():
                    self.issues.append(Issue(
                        filepath=filepath,
                        severity='error',
                        message=f"Broken wikilink at line {lineno}: [[{link_path}]] -> {target_path} does not exist",
                        fix_available=False
                    ))

    def _resolve_wikilink(self, source_file: Path, link: str) -> Optional[Path]:
        """Resolve a wikilink to an absolute path.

        Args:
            source_file: The file containing the wikilink
            link: The wikilink path (e.g., '../code/file.py' or 'concept-name')

        Returns:
            Absolute path to the linked file, or None if link format is invalid
        """
        # Handle relative paths (contain ../ or ./)
        if link.startswith('../') or link.startswith('./'):
            # Relative to the source file's directory
            resolved = (source_file.parent / link).resolve()
            return resolved

        # Handle absolute-looking paths that start from vault root
        if '/' in link:
            # Treat as path from vault root
            resolved = (self.vault_path / link).resolve()
            return resolved

        # Plain filename - search in multiple locations
        # 1. Same directory as source
        same_dir = source_file.parent / link
        if not link.endswith('.md') and not link.endswith('.py'):
            # Try adding .md extension for markdown files
            same_dir_md = source_file.parent / f"{link}.md"
            if same_dir_md.exists():
                return same_dir_md.resolve()

        if same_dir.exists():
            return same_dir.resolve()

        # 2. obsidian/ directory for concept/pattern files
        obsidian_path = self.vault_path / 'obsidian' / link
        if not link.endswith('.md'):
            obsidian_path_md = self.vault_path / 'obsidian' / f"{link}.md"
            if obsidian_path_md.exists():
                return obsidian_path_md.resolve()

        if obsidian_path.exists():
            return obsidian_path.resolve()

        # 3. code/ directory for Python files
        code_path = self.vault_path / 'code' / link
        if not link.endswith('.py'):
            code_path_py = self.vault_path / 'code' / f"{link}.py"
            if code_path_py.exists():
                return code_path_py.resolve()

        if code_path.exists():
            return code_path.resolve()

        # If we get here, return the "expected" path for error reporting
        # Default to same directory if no extension, otherwise use as-is
        if '.' not in link:
            return source_file.parent / f"{link}.md"
        return source_file.parent / link

    def scan_repository(self) -> None:
        """Scan all files in the repository."""
        # Phase 1: Scan Python files and collect block markers
        for py_file in (self.vault_path / 'code').rglob('*.py'):
            self.validate_python_file(py_file)

            # Extract wikilinks from Python docstrings
            try:
                content = py_file.read_text(encoding='utf-8')
                self.extract_wikilinks(py_file, content)
            except Exception:
                pass  # Already reported in validate_python_file

        # Phase 2: Scan markdown files and collect block marker references
        for md_file in self.vault_path.rglob('*.md'):
            # Skip hidden directories and whiteboard folder
            if any(part.startswith('.') for part in md_file.parts):
                continue
            if 'whiteboard' in md_file.parts:
                continue

            # Validate markdown file
            self.validate_markdown_file(md_file)

            # Extract block marker references and wikilinks
            try:
                content = md_file.read_text(encoding='utf-8')
                self.extract_block_marker_references(md_file, content)
                self.extract_wikilinks(md_file, content)
            except Exception:
                pass  # Already reported in validate_markdown_file

        # Phase 3: Validate all block marker references resolve
        self.validate_all_block_marker_references()

    def _get_issue_type_tag(self, issue: Issue) -> str:
        """Determine issue type tag based on the problem."""
        message = issue.message.lower()

        if "missing yaml frontmatter" in message or "missing frontmatter" in message:
            return "missing-frontmatter"
        elif "missing required tag" in message:
            return "missing-required-tag"
        elif "missing type/" in message:
            return "missing-type-tag"
        elif "missing recommended tags" in message:
            return "missing-recommended-tags"
        elif "inline array format" in message:
            return "tag-format-warning"
        elif "missing block marker" in message:
            return "missing-block-marker"
        elif "duplicate block marker" in message:
            return "duplicate-block-marker"
        elif "incorrect block marker" in message:
            return "incorrect-block-marker"
        elif "orphaned block marker" in message:
            return "orphaned-block-marker"
        elif "dead block marker reference" in message:
            return "dead-block-reference"
        elif "broken wikilink" in message:
            return "broken-wikilink"
        elif "docstring" in message:
            return "docstring-issue"
        elif "schema" in message:
            return "schema-violation"
        else:
            return "other"

    def _get_issue_context(self, issue: Issue) -> str:
        """Provide context about what's wrong and what's expected."""
        message = issue.message.lower()

        if "missing yaml frontmatter" in message:
            if issue.filepath.suffix == '.py':
                return """**What's wrong**: This Python file lacks YAML frontmatter in its module docstring.

**What's expected**: Python code files must have a module-level docstring that starts with YAML frontmatter containing tags. The frontmatter must include:
- `type/code-file` tag (required)
- At least one `domain/*` tag (recommended)
- At least one `layer/*` tag (recommended)

The docstring should follow this structure:
1. YAML frontmatter with tags
2. Module name header
3. Purpose section
4. Related documentation links
5. Dependencies

See CLAUDE.md for the complete schema."""
            else:
                return """**What's wrong**: This markdown file lacks YAML frontmatter.

**What's expected**: All markdown documentation files must start with YAML frontmatter containing tags. The frontmatter defines:
- File type (type/concept, type/pattern, or type/index)
- Domain tags indicating the problem domain
- Layer tags indicating the architectural layer

See CLAUDE.md for the complete schema and tag hierarchy."""

        elif "inline array format" in message:
            return """**What's wrong**: Tags are using inline array format: `tags: [tag1, tag2, tag3]`

**What's expected**: For better Obsidian compatibility, especially with hierarchical tags using slashes (like `type/concept`, `domain/mathematics`), use YAML list format:

```yaml
---
tags:
  - type/concept
  - domain/mathematics
  - layer/core
---
```

**Why**: Obsidian's tag system works best with YAML list format for hierarchical tags. The inline array format may not properly parse nested tags with slashes.

**How to fix**: Convert from:
```yaml
tags: [type/concept, domain/mathematics]
```

To:
```yaml
tags:
  - type/concept
  - domain/mathematics
```"""

        elif "missing required tag" in message:
            tag_match = re.search(r"Missing required tag: (.+)$", issue.message)
            required_tag = tag_match.group(1) if tag_match else "unknown"
            return f"""**What's wrong**: The file's frontmatter is missing the required tag: `{required_tag}`

**What's expected**: Based on the file type, certain tags are mandatory:
- Python files must have: `type/code-file`
- Concept files must have: `type/concept`
- Pattern files must have: `type/pattern`
- Index files must have: `type/index`

The tags array in the frontmatter must include this required tag."""

        elif "missing type/" in message:
            return """**What's wrong**: The file has frontmatter but no `type/*` tag.

**What's expected**: Every file must have exactly one type tag that categorizes it:
- `type/code-file` - Python source code
- `type/concept` - Conceptual/domain documentation
- `type/pattern` - Design pattern documentation
- `type/index` - Index or overview file

The type tag determines what other required tags are needed."""

        elif "missing recommended tags" in message:
            return """**What's wrong**: The file meets minimum requirements but lacks recommended tags.

**What's expected**: While not required, these tags improve organization:
- `domain/*` - Indicates the problem domain (e.g., domain/mathematics, domain/ui)
- `layer/*` - Indicates architectural layer (e.g., layer/core, layer/interface)
- `pattern/*` - Indicates design patterns used (e.g., pattern/strategy)

These tags enable better filtering and organization in Obsidian's graph view."""

        else:
            return f"""**What's wrong**: {issue.message}

**What's expected**: Refer to CLAUDE.md for the complete schema and requirements for this repository."""

    def write_individual_issues(self) -> None:
        """Write each issue to a separate file in whiteboard/janitor/ folder."""
        janitor_dir = self.vault_path / 'whiteboard' / 'janitor'

        # Clear out old issues
        if janitor_dir.exists():
            import shutil
            shutil.rmtree(janitor_dir)

        # Create fresh janitor directory
        janitor_dir.mkdir(parents=True, exist_ok=True)

        if not self.issues:
            print(f"\nNo issues found. {janitor_dir.relative_to(self.vault_path)}/ is empty.")
            return

        # Write each issue to a separate file
        for idx, issue in enumerate(self.issues, start=1):
            # Create filename: 01-error-filename.md or 01-warning-filename.md
            severity_prefix = issue.severity
            file_stem = issue.filepath.stem.replace(' ', '-')
            issue_filename = f"{idx:02d}-{severity_prefix}-{file_stem}.md"
            issue_path = janitor_dir / issue_filename

            # Build the issue content
            rel_path = issue.filepath.relative_to(self.vault_path)
            obsidian_link = f"[[{rel_path}|{issue.filepath.name}]]"

            # Determine issue type tag based on problem
            issue_type = self._get_issue_type_tag(issue)

            lines = [
                "---",
                f"tags: [janitor-issue, janitor-issue/{issue_type}, severity/{issue.severity}]",
                "---",
                "",
                f"# Issue #{idx}: {issue.filepath.name}",
                "",
                f"**File**: {obsidian_link}",
                "",
                f"**Severity**: {issue.severity.upper()}",
                "",
                f"**Path**: `{rel_path}`",
                "",
                "## Problem",
                "",
                issue.message,
                "",
            ]

            # Add context about what's wrong and what's expected
            lines.extend([
                "## Context",
                "",
                self._get_issue_context(issue),
                "",
            ])

            if issue.fix_available:
                lines.extend([
                    "## Note",
                    "",
                    f"Auto-fix available: `{issue.fix_description}`",
                    "",
                    "Run `python janitor.py --fix` to apply automatically.",
                    "",
                ])

            issue_path.write_text('\n'.join(lines), encoding='utf-8')

        print(f"\n{len(self.issues)} issue files written to {janitor_dir.relative_to(self.vault_path)}/")

    def write_report(self) -> None:
        """Write summary report to whiteboard/janitor/00-summary.md."""
        janitor_dir = self.vault_path / 'whiteboard' / 'janitor'
        report_path = janitor_dir / '00-summary.md'

        # Ensure janitor directory exists
        janitor_dir.mkdir(parents=True, exist_ok=True)

        errors = [i for i in self.issues if i.severity == 'error']
        warnings = [i for i in self.issues if i.severity == 'warning']

        # Build markdown report
        lines = [
            "---",
            "tags: [janitor-report, type/index]",
            "---",
            "",
            "# Janitor Report",
            "",
            f"**Generated**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        if not self.issues:
            lines.extend([
                "## Status",
                "",
                "**Repository is healthy!** No issues found.",
                "",
            ])
        else:
            lines.extend([
                "## Summary",
                "",
                f"- **Errors**: {len(errors)}",
                f"- **Warnings**: {len(warnings)}",
                f"- **Total Issues**: {len(self.issues)}",
                "",
            ])

            if errors:
                lines.extend([
                    "## Errors",
                    "",
                ])
                for issue in errors:
                    rel_path = issue.filepath.relative_to(self.vault_path)
                    # Create Obsidian wikilink to the file
                    obsidian_link = f"[[{rel_path}|{issue.filepath.name}]]"
                    lines.append(f"### {obsidian_link}")
                    lines.append("")
                    lines.append(f"**File**: `{rel_path}`")
                    lines.append("")
                    lines.append(f"**Problem**: {issue.message}")
                    lines.append("")
                    if issue.fix_available:
                        lines.append(f"**Auto-fix available**: Run `python janitor.py --fix`")
                        lines.append("")

            if warnings:
                lines.extend([
                    "## Warnings",
                    "",
                ])
                for issue in warnings:
                    rel_path = issue.filepath.relative_to(self.vault_path)
                    # Create Obsidian wikilink to the file
                    obsidian_link = f"[[{rel_path}|{issue.filepath.name}]]"
                    lines.append(f"### {obsidian_link}")
                    lines.append("")
                    lines.append(f"**File**: `{rel_path}`")
                    lines.append("")
                    lines.append(f"**Problem**: {issue.message}")
                    lines.append("")
                    if issue.fix_available:
                        lines.append(f"**Auto-fix available**: Run `python janitor.py --fix`")
                        lines.append("")

        # Write report
        report_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"\nReport written to {report_path.relative_to(self.vault_path)}")

    def report_issues(self) -> None:
        """Print all found issues to console."""
        if not self.issues:
            print("No issues found! Repository is healthy.")
            return

        errors = [i for i in self.issues if i.severity == 'error']
        warnings = [i for i in self.issues if i.severity == 'warning']

        if errors:
            print(f"\n{len(errors)} ERROR(S) FOUND:\n")
            for issue in errors:
                print(f"  {issue.filepath.relative_to(self.vault_path)}")
                print(f"    {issue.message}")
                if issue.fix_available:
                    print(f"    Fix: {issue.fix_description}")
                print()

        if warnings:
            print(f"\n{len(warnings)} WARNING(S) FOUND:\n")
            for issue in warnings:
                print(f"  {issue.filepath.relative_to(self.vault_path)}")
                print(f"    {issue.message}")
                if issue.fix_available:
                    print(f"    Fix: {issue.fix_description}")
                print()

    def apply_fixes(self, auto_yes: bool = False) -> int:
        """Apply automatic fixes to issues."""
        fixable = [i for i in self.issues if i.fix_available and i.auto_fix_fn]

        if not fixable:
            print("\nNo auto-fixable issues found.")
            return 0

        print(f"\n{len(fixable)} issue(s) can be auto-fixed:")
        for issue in fixable:
            print(f"  - {issue.filepath.relative_to(self.vault_path)}: {issue.fix_description}")

        if not auto_yes:
            response = input("\nApply these fixes? [y/N] ").strip().lower()
            if response != 'y':
                print("Fixes cancelled.")
                return 0

        fixed_count = 0
        for issue in fixable:
            try:
                if issue.auto_fix_fn():
                    print(f"  ✓ Fixed: {issue.filepath.name}")
                    fixed_count += 1
                else:
                    print(f"  ✗ Could not fix: {issue.filepath.name}")
            except Exception as e:
                print(f"  ✗ Error fixing {issue.filepath.name}: {e}")

        print(f"\n✓ Fixed {fixed_count} issue(s)")
        return fixed_count


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Repository health checker and fixer')
    parser.add_argument('--fix', action='store_true', help='Apply automatic fixes')
    parser.add_argument('--yes', '-y', action='store_true', help='Auto-confirm fixes')
    args = parser.parse_args()

    # Script is in maintenance_scripts/, root is parent
    vault_path = Path(__file__).parent.parent
    janitor = RepositoryJanitor(vault_path)

    print("Scanning repository...\n")
    janitor.scan_repository()
    janitor.report_issues()
    janitor.write_individual_issues()
    janitor.write_report()

    if args.fix:
        janitor.apply_fixes(auto_yes=args.yes)


if __name__ == '__main__':
    main()
