---
tags:
  - type/pattern
  - domain/automation
  - category/analytics
  - category/best-practices
---

# Knowledge Graph Metrics System

## Overview

The graph metrics system analyzes the Obsidian knowledge graph for potential scaling pathologies and health issues. It provides actionable insights without prescribing hard rules.

**Key Principle**: These are metrics to inform decisions, not targets to hit.

## What It Detects

### Oversized Tags (≥15 files)

Tags with many files may benefit from hierarchical subdivision.

**Example**: `#type/code-file` with 121 files
- **Action**: Consider `#type/code-file/application`, `#type/code-file/test`, `#type/code-file/infrastructure`
- **Note**: AST cache files inherit tags, inflating counts - this is expected

### Undersized Tags (≤2 files)

Non-type tags with very few files may indicate over-granularity.

**Example**: `#category/code-generation` with 1 file
- **Question**: Is this too specific, or a new area that will grow?
- **Action**: Monitor over time; consolidate if it stays small

### Low Wikilink Density

Files with fewer wikilinks than recommended:
- Code files: Should have ≥1 wikilink (to concepts/patterns)
- Documentation: Should have ≥2 wikilinks (to other docs/code)

**Purpose**: Ensure files are integrated into the knowledge graph

### Orphaned Files

Files with no tags at all.

**Impact**: These files don't appear in tag-based navigation or graph views

### Tag Hierarchy Gaps

Single-level tags with many files that might benefit from subcategories.

**Example**: `#domain/mathematics` → Consider `#domain/mathematics/algebra`, `#domain/mathematics/calculus`

## How It Works

### Integration Point

The graph metrics analyzer runs as **Step 3** in the update workflow:

```bash
uv run update.py
```

**Workflow**:
1. Generate AST cache (creates searchable representations of code)
2. Generate tag indices (creates repository-map and tag-index)
3. **Generate graph metrics** (analyzes graph health) ← New step
4. Run janitor health checks (validates schema compliance)

### Report Location

The report is always written to:

```
whiteboard/graph-metrics.md
```

**Why whiteboard?**
- High visibility for ongoing work
- Not part of permanent documentation
- Represents current state snapshot

### What Gets Analyzed

The analyzer scans:
- All `.py` files (including root-level infrastructure scripts)
- All `.md` files (excluding auto-generated indices)
- AST cache files (`.ast.md` - inherit source file tags)

**Excluded**:
- `.git/`, `.obsidian/`, `__pycache__/`
- `whiteboard/` (metrics don't analyze themselves)
- `index/` directory (repository-map and tag-index)

## Implementation

### Core Script

[[../graph_metrics.py|graph_metrics.py]] - Knowledge graph analyzer

**Key classes**:
- `GraphMetricsAnalyzer` - Main analysis engine
- `TagMetrics` - Metrics for a single tag
- `FileMetrics` - Metrics for a single file

### Analysis Methods

```python
analyze_tag_sizes()         # Oversized and undersized tags
analyze_orphaned_files()    # Files with no tags
analyze_wikilink_density()  # Files with too few wikilinks
analyze_tag_hierarchy_gaps()# Tags needing subcategories
analyze_tag_distribution()  # Tag counts by hierarchy
```

### Configurable Thresholds

```python
OVERSIZED_TAG_THRESHOLD = 15    # Tag with >15 files
UNDERSIZED_TAG_THRESHOLD = 2    # Tag with <2 files
MIN_WIKILINKS_FOR_CODE = 1      # Code should link to concepts
MIN_WIKILINKS_FOR_DOCS = 2      # Docs should link to docs/code
```

**Note**: These can be adjusted based on project needs

## Interpreting Results

### Oversized Tags

**Not always a problem**:
- AST cache files inflate counts (every function/class gets a file)
- Some domains are naturally large
- Infrastructure tags may cover many files

**When to split**:
- Files represent distinct subcategories
- Navigation becomes difficult
- Team wants finer-grained filtering

### Undersized Tags

**Not always a problem**:
- New areas naturally start small
- Very specific concepts may only apply to 1-2 files
- Infrastructure categories may be intentionally narrow

**When to consolidate**:
- Tag hasn't grown over time
- Could be merged into broader category
- Adds noise without value

### Low Wikilink Density

**Expected for**:
- Brand new files
- Infrastructure scripts (often self-contained)
- Entry point files

**Actionable for**:
- Documentation files (should link to implementation)
- Code files (should link to concepts/patterns they implement)

### Zero Orphaned Files

**Current state**: All files are tagged ✅

**How we got here**:
- Python files use custom docstring format with inline tags
- Markdown files use YAML frontmatter
- Infrastructure scripts tagged with `#domain/automation #layer/infrastructure`

## Common Patterns

### AST Cache Inflation

AST cache files inherit all tags from source files:

**Source**: `code/operations.py` with `#domain/mathematics`
**AST cache**: 25 function files, each with `#domain/mathematics`
**Result**: `#domain/mathematics` shows 26 files (1 source + 25 AST)

**This is expected** - AST files make code searchable in Obsidian graph

### Test File Clustering

Test files naturally cluster:
- `#domain/testing` - 84 files
- `#layer/test` - 83 files
- `#category/unit-test` - 83 files

**This is healthy** - tests are a major part of the codebase

### Infrastructure Tags

Infrastructure scripts use specific categories:
- `#category/code-generation` - [[../generate_ast.py]]
- `#category/indexing` - [[../generate_tags.py]]
- `#category/analytics` - [[../graph_metrics.py]]
- `#category/validation` - [[../janitor.py]]
- `#category/orchestration` - [[../update.py]]

**Small counts are fine** - each category has 1-2 files by design

## Best Practices

### When to Act on Metrics

✅ **Do**:
- Use metrics to inform architecture decisions
- Identify areas needing documentation
- Find files missing connections to knowledge graph
- Track growth patterns over time

❌ **Don't**:
- Treat thresholds as hard rules
- Split tags just to reduce counts
- Force wikilinks where they don't make sense
- Ignore domain context

### Maintaining Health

**Regular workflow**:
```bash
# After making changes
uv run update.py

# Review metrics
cat whiteboard/graph-metrics.md
```

**Questions to ask**:
- Are oversized tags growing out of control?
- Do new files have appropriate tags?
- Are wikilinks creating useful connections?
- Do tag hierarchies match mental models?

### Evolution Over Time

**Archive old reports** if you want to track trends:
```bash
cp whiteboard/graph-metrics.md whiteboard/archive/graph-metrics-2025-10-20.md
```

**Compare reports** to see:
- Which tags are growing fastest
- Whether refactorings improved structure
- If new patterns are emerging

## Related Documentation

- Implementation: [[../graph_metrics.py|Graph Metrics Analyzer]]
- Workflow: [[../update.py|Update Workflow]]
- Tag System: [[../CLAUDE.md#Tag System|CLAUDE.md - Tag System]]
- Validation: [[../janitor.py|Repository Health Janitor]]

## Philosophy

Good metrics are:
- **Informative** - Show what's actually happening
- **Contextual** - Consider domain and purpose
- **Actionable** - Suggest specific improvements
- **Non-prescriptive** - Guide without mandating

The graph metrics system embodies this philosophy by providing visibility without enforcement.
