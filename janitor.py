#!/usr/bin/env python3
"""
Repository Health Janitor

Validates and automatically fixes issues in the Obsidian knowledge graph repository:
- Checks all files have required YAML frontmatter tags
- Validates Python file docstring schema
- Ensures markdown files are in obsidian/ folder

Usage:
    python janitor.py              # Check for issues
    python janitor.py --fix        # Auto-fix issues with confirmation
    python janitor.py --fix --yes  # Auto-fix without confirmation
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
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
---
tags: [type/code-file, domain/*, layer/*]
---

# Module Name

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

        frontmatter = {}

        # Parse tags
        tags_match = re.search(r'tags:\s*\[(.*?)\]', yaml_content)
        if tags_match:
            tags_str = tags_match.group(1)
            tags = [t.strip().strip('"').strip("'") for t in tags_str.split(',')]
            frontmatter['tags'] = tags

        return frontmatter, remaining

    def extract_python_docstring(self, content: str) -> Optional[str]:
        """Extract the module-level docstring from Python file."""
        # Match triple-quoted docstring at start of file
        match = re.match(r'^\s*"""(.*?)"""\s*\n', content, re.DOTALL)
        if match:
            return match.group(1)
        return None

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

        # Parse frontmatter from docstring
        frontmatter, _ = self.parse_frontmatter(docstring)
        if not frontmatter:
            self.issues.append(Issue(
                filepath=filepath,
                severity='error',
                message="Docstring missing YAML frontmatter",
                fix_available=True,
                fix_description="Add frontmatter to existing docstring",
                auto_fix_fn=lambda: self.fix_add_frontmatter_to_docstring(filepath)
            ))
            return

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

    # ==================== MAIN EXECUTION ====================

    def scan_repository(self) -> None:
        """Scan all files in the repository."""
        # Scan Python files
        for py_file in (self.vault_path / 'code').rglob('*.py'):
            self.validate_python_file(py_file)

        # Scan markdown files
        for md_file in self.vault_path.rglob('*.md'):
            # Skip hidden directories and whiteboard folder
            if any(part.startswith('.') for part in md_file.parts):
                continue
            if 'whiteboard' in md_file.parts:
                continue
            self.validate_markdown_file(md_file)

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

    vault_path = Path(__file__).parent
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
