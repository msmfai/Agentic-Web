#!/usr/bin/env python3
"""
# Knowledge Graph Metrics Analyzer

**Tags**: #type/code-file #domain/automation #layer/infrastructure #category/analytics

## Purpose
Analyze knowledge graph for potential scaling pathologies.

This script analyzes the knowledge graph for:
- Oversized tags (tags with too many files)
- Undersized tags (tags with only 1-2 files that should maybe be consolidated)
- Missing hierarchical splits (broad tags that need subcategories)
- Orphaned files (files with no tags)
- Tag distribution imbalances
- Wikilink density issues

Outputs metrics report to whiteboard/ for visibility.

Usage:
    python graph_metrics.py
    uv run graph_metrics.py
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass


@dataclass
class TagMetrics:
    """Metrics for a single tag."""
    tag: str
    file_count: int
    files: List[Path]


@dataclass
class FileMetrics:
    """Metrics for a single file."""
    path: Path
    tag_count: int
    wikilink_count: int
    tags: List[str]


class GraphMetricsAnalyzer:
    """Analyzes knowledge graph structure and health."""

    # Thresholds for warnings
    OVERSIZED_TAG_THRESHOLD = 15  # Tag with >15 files may need splitting
    UNDERSIZED_TAG_THRESHOLD = 2  # Tag with <2 files may be too granular
    MIN_WIKILINKS_FOR_CODE = 1  # Code files should link to concepts
    MIN_WIKILINKS_FOR_DOCS = 2  # Doc files should link to other docs/code

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.tags_to_files: Dict[str, List[Path]] = defaultdict(list)
        self.file_to_tags: Dict[Path, List[str]] = {}
        self.file_to_wikilinks: Dict[Path, int] = {}
        self.all_tags: Set[str] = set()
        # Don't skip ast-cache since we want to count those files for tag coverage
        self.skip_dirs = {'.git', '.obsidian', '__pycache__', 'node_modules', '.venv', 'venv', 'whiteboard', 'index'}

    def parse_yaml_frontmatter(self, content: str) -> List[str]:
        """Extract tags from YAML frontmatter."""
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return []

        yaml_content = match.group(1)

        # Try inline array format
        tags_match_inline = re.search(r'tags:\s*\[(.*?)\]', yaml_content)
        if tags_match_inline:
            tags_str = tags_match_inline.group(1)
            return [t.strip().strip('"').strip("'") for t in tags_str.split(',')]

        # Try YAML list format
        tags_match_list = re.search(r'tags:\s*\n((?:\s+-\s+.+\n?)+)', yaml_content)
        if tags_match_list:
            tags_str = tags_match_list.group(1)
            return [line.strip().lstrip('-').strip() for line in tags_str.strip().split('\n')]

        return []

    def parse_python_docstring_tags(self, content: str) -> List[str]:
        """Extract tags from Python custom frontmatter format.

        Supports both old and new formats:
        - Old: **Tags**: #tag1 #tag2 #tag3
        - New: **File Tags**: #tag1
               **Inheritable Tags**: #tag2 #tag3
        """
        # Skip shebang line if present
        lines = content.split('\n', 1)
        if lines[0].startswith('#!'):
            content_to_parse = lines[1] if len(lines) > 1 else ''
        else:
            content_to_parse = content

        match = re.match(r'^\s*"""(.*?)"""\s*\n', content_to_parse, re.DOTALL)
        if not match:
            return []

        docstring = match.group(1)
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
        else:
            # Fallback to old format (**Tags**: #tag1 #tag2 #tag3)
            tags_match = re.search(r'\*\*Tags\*\*:\s*(.+)$', docstring, re.MULTILINE)
            if tags_match:
                tags_line = tags_match.group(1)
                all_tags = re.findall(r'#([\w/.-]+)', tags_line)

        tags = all_tags
        return tags

    def count_wikilinks(self, content: str) -> int:
        """Count wikilinks in file content."""
        # Match [[link]] or [[link|display]]
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
        return len(wikilinks)

    def should_skip_path(self, path: Path) -> bool:
        """Check if a path should be skipped."""
        for part in path.parts:
            if part in self.skip_dirs:
                return True
        return False

    def scan_file(self, filepath: Path) -> None:
        """Scan a single file for tags and wikilinks."""
        if self.should_skip_path(filepath):
            return

        try:
            content = filepath.read_text(encoding='utf-8')
            tags = []
            wikilinks = self.count_wikilinks(content)

            # Extract tags based on file type
            if filepath.suffix == '.py':
                tags = self.parse_python_docstring_tags(content)
            elif filepath.suffix == '.md':
                tags = self.parse_yaml_frontmatter(content)

            # Store metrics
            if tags or wikilinks > 0:
                self.file_to_tags[filepath] = tags
                self.file_to_wikilinks[filepath] = wikilinks

                for tag in tags:
                    self.tags_to_files[tag].append(filepath)
                    self.all_tags.add(tag)

        except Exception as e:
            pass  # Silently skip files we can't parse

    def scan_repository(self) -> None:
        """Scan entire repository."""
        for filepath in self.root_dir.rglob('*'):
            if filepath.is_file():
                self.scan_file(filepath)

    def analyze_tag_sizes(self) -> Tuple[List[TagMetrics], List[TagMetrics]]:
        """Identify oversized and undersized tags."""
        oversized = []
        undersized = []

        for tag, files in self.tags_to_files.items():
            file_count = len(files)

            # Skip auto-generated and infrastructure tags
            if tag in ['auto-generated', 'type/index', 'type/ast-node', 'purpose/llm-instructions']:
                continue

            if file_count >= self.OVERSIZED_TAG_THRESHOLD:
                oversized.append(TagMetrics(tag, file_count, files))
            elif file_count <= self.UNDERSIZED_TAG_THRESHOLD and not tag.startswith('type/'):
                undersized.append(TagMetrics(tag, file_count, files))

        # Sort by file count
        oversized.sort(key=lambda x: x.file_count, reverse=True)
        undersized.sort(key=lambda x: x.file_count)

        return oversized, undersized

    def analyze_orphaned_files(self) -> List[Path]:
        """Find files with no tags."""
        orphaned = []
        for filepath in self.root_dir.rglob('*'):
            if filepath.is_file() and not self.should_skip_path(filepath):
                if filepath.suffix in ['.py', '.md']:
                    if filepath not in self.file_to_tags or not self.file_to_tags[filepath]:
                        orphaned.append(filepath)
        return orphaned

    def analyze_wikilink_density(self) -> List[FileMetrics]:
        """Find files with low wikilink density."""
        low_density = []

        for filepath, wikilink_count in self.file_to_wikilinks.items():
            tags = self.file_to_tags.get(filepath, [])

            # Skip auto-generated files
            if 'auto-generated' in tags or 'type/ast-node' in tags:
                continue

            # Check thresholds
            is_code = filepath.suffix == '.py'
            is_docs = filepath.suffix == '.md'

            if is_code and wikilink_count < self.MIN_WIKILINKS_FOR_CODE:
                low_density.append(FileMetrics(filepath, len(tags), wikilink_count, tags))
            elif is_docs and wikilink_count < self.MIN_WIKILINKS_FOR_DOCS:
                low_density.append(FileMetrics(filepath, len(tags), wikilink_count, tags))

        return low_density

    def analyze_tag_hierarchy_gaps(self) -> Dict[str, List[str]]:
        """Identify tag hierarchies that might benefit from more levels."""
        hierarchy_analysis = defaultdict(list)

        # Group tags by their root hierarchy
        for tag in self.all_tags:
            if '/' in tag:
                parts = tag.split('/')
                root = parts[0]

                # If tag has only 1 level and many files, it might need subcategories
                if len(parts) == 1:
                    file_count = len(self.tags_to_files[tag])
                    if file_count >= self.OVERSIZED_TAG_THRESHOLD:
                        hierarchy_analysis[root].append(f"{tag} ({file_count} files) - consider subcategories")

        return dict(hierarchy_analysis)

    def analyze_tag_distribution(self) -> Dict[str, int]:
        """Analyze distribution of tags across hierarchies."""
        hierarchy_counts = defaultdict(int)

        for tag in self.all_tags:
            if '/' in tag:
                prefix = tag.split('/', 1)[0]
            else:
                prefix = 'no-hierarchy'
            hierarchy_counts[prefix] += 1

        return dict(sorted(hierarchy_counts.items(), key=lambda x: x[1], reverse=True))

    def generate_report(self) -> str:
        """Generate comprehensive metrics report."""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        oversized_tags, undersized_tags = self.analyze_tag_sizes()
        orphaned_files = self.analyze_orphaned_files()
        low_density_files = self.analyze_wikilink_density()
        hierarchy_gaps = self.analyze_tag_hierarchy_gaps()
        tag_distribution = self.analyze_tag_distribution()

        lines = [
            "# Knowledge Graph Metrics Report",
            "",
            "**Auto-generated metrics - not targets**",
            "",
            f"**Generated**: {now}",
            "",
            "This report identifies potential scaling pathologies in the knowledge graph. These are metrics to inform decisions, not hard rules to follow.",
            "",
            "---",
            "",
            "## Overview",
            "",
            f"- Total unique tags: {len(self.all_tags)}",
            f"- Total tagged files: {len(self.file_to_tags)}",
            f"- Average tags per file: {sum(len(tags) for tags in self.file_to_tags.values()) / len(self.file_to_tags):.1f}" if self.file_to_tags else "- Average tags per file: 0",
            "",
            "## Tag Distribution by Hierarchy",
            "",
        ]

        for hierarchy, count in tag_distribution.items():
            lines.append(f"- `{hierarchy}/*`: {count} tags")

        lines.extend([
            "",
            "---",
            "",
            "## ⚠️ Oversized Tags",
            "",
            f"Tags with ≥{self.OVERSIZED_TAG_THRESHOLD} files may benefit from hierarchical subdivision.",
            "",
        ])

        if oversized_tags:
            for metric in oversized_tags:
                lines.append(f"### `#{metric.tag}` ({metric.file_count} files)")
                lines.append("")
                lines.append("**Potential actions**:")
                lines.append(f"- Consider splitting into subcategories: `{metric.tag}/subcategory`")
                lines.append("- Review if all files truly belong to this category")
                lines.append("- Consider if this represents multiple distinct concepts")
                lines.append("")
                lines.append("**Files**:")
                for f in metric.files[:10]:  # Show first 10
                    rel_path = f.relative_to(self.root_dir)
                    lines.append(f"- {rel_path}")
                if len(metric.files) > 10:
                    lines.append(f"- ... and {len(metric.files) - 10} more")
                lines.append("")
        else:
            lines.append("✅ No oversized tags detected")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 🔍 Undersized Tags",
            "",
            f"Non-type tags with ≤{self.UNDERSIZED_TAG_THRESHOLD} files. May indicate over-granularity.",
            "",
        ])

        if undersized_tags:
            # Group by count
            by_count = defaultdict(list)
            for metric in undersized_tags:
                by_count[metric.file_count].append(metric.tag)

            for count in sorted(by_count.keys()):
                tags = by_count[count]
                lines.append(f"**{count} file{'s' if count != 1 else ''}**: {', '.join(f'`#{t}`' for t in tags)}")
            lines.append("")
            lines.append("**Considerations**:")
            lines.append("- Are these tags too specific?")
            lines.append("- Could they be consolidated into broader categories?")
            lines.append("- Or are they simply new areas that will grow?")
            lines.append("")
        else:
            lines.append("✅ No undersized tags detected")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 🔗 Low Wikilink Density",
            "",
            f"Files with fewer wikilinks than recommended (code: {self.MIN_WIKILINKS_FOR_CODE}, docs: {self.MIN_WIKILINKS_FOR_DOCS}).",
            "",
        ])

        if low_density_files:
            lines.append("These files might benefit from more connections to the knowledge graph:")
            lines.append("")
            for metric in low_density_files[:20]:  # Show first 20
                rel_path = metric.path.relative_to(self.root_dir)
                lines.append(f"- `{rel_path}` - {metric.wikilink_count} wikilink{'s' if metric.wikilink_count != 1 else ''}")
            if len(low_density_files) > 20:
                lines.append(f"- ... and {len(low_density_files) - 20} more")
            lines.append("")
        else:
            lines.append("✅ All files have adequate wikilink density")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 📋 Orphaned Files",
            "",
            "Files with no tags (excluding auto-generated files).",
            "",
        ])

        if orphaned_files:
            lines.append("These files are not integrated into the tag system:")
            lines.append("")
            for filepath in orphaned_files[:20]:  # Show first 20
                rel_path = filepath.relative_to(self.root_dir)
                lines.append(f"- `{rel_path}`")
            if len(orphaned_files) > 20:
                lines.append(f"- ... and {len(orphaned_files) - 20} more")
            lines.append("")
        else:
            lines.append("✅ No orphaned files detected")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 📊 Tag Hierarchy Health",
            "",
            "Analysis of tag hierarchies that might benefit from additional levels.",
            "",
        ])

        if hierarchy_gaps:
            for root, issues in hierarchy_gaps.items():
                lines.append(f"### `{root}/*` hierarchy")
                lines.append("")
                for issue in issues:
                    lines.append(f"- {issue}")
                lines.append("")
        else:
            lines.append("✅ Tag hierarchies look healthy")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## Summary",
            "",
            f"- Oversized tags: **{len(oversized_tags)}**",
            f"- Undersized tags: **{len(undersized_tags)}**",
            f"- Low-density files: **{len(low_density_files)}**",
            f"- Orphaned files: **{len(orphaned_files)}**",
            "",
            "**Remember**: These are metrics to inform judgment, not strict rules. Context matters.",
            "",
        ])

        return '\n'.join(lines)

    def write_report(self) -> Path:
        """Write metrics report to whiteboard."""
        whiteboard_dir = self.root_dir / "whiteboard"
        whiteboard_dir.mkdir(exist_ok=True)

        report_path = whiteboard_dir / "graph-metrics.md"
        report_content = self.generate_report()
        report_path.write_text(report_content, encoding='utf-8')

        return report_path


def main():
    root_dir = Path(__file__).parent

    print()
    print("=" * 60)
    print("Knowledge Graph Metrics Analyzer")
    print("=" * 60)
    print()
    print(f"Root directory: {root_dir}")
    print()

    analyzer = GraphMetricsAnalyzer(root_dir)

    print("Scanning repository...")
    analyzer.scan_repository()

    print(f"Found {len(analyzer.all_tags)} tags across {len(analyzer.file_to_tags)} files")
    print()

    print("Analyzing graph structure...")
    report_path = analyzer.write_report()

    print()
    print(f"Report written to: {report_path.relative_to(root_dir)}")
    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
