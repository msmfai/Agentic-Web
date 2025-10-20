---
tags: [type/FIXME]
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a **unified code-documentation system** using Obsidian as a knowledge graph. Code and documentation are interconnected through bidirectional wikilinks, creating a navigable web of understanding.

### Directory Structure

- `code/` - Python source files (follows standard Python conventions)
- `obsidian/` - Documentation markdown files (flat structure, no subdirectories)
- `.obsidian/` - Obsidian configuration

**Key Principle**: Code stays in `code/` with whatever structure the compiler/tooling requires. Documentation lives flat in `obsidian/`. Organization is driven by tags, not filesystem hierarchy.

### The Obsidian Integration

This system uses **Custom File Extensions Plugin** to make `.py` files participate in Obsidian's graph view as markdown nodes. This allows:

1. Wikilinks in Python docstrings become graph edges
2. Code files appear as nodes in the knowledge graph
3. Bidirectional navigation between code ↔ concepts ↔ patterns

## Tag System (CRITICAL)

All files MUST have YAML frontmatter with hierarchical tags. Tags are the primary organizational system.

### Required Tags by File Type

**Python Code Files** (`.py` in `code/`):

```yaml
---
tags: [type/code-file, domain/*, layer/*, pattern/*]
---
```

- **MUST have**: `type/code-file` (required for filtering code nodes)
- **SHOULD have**: At least one `domain/*` tag (e.g., `domain/mathematics`, `domain/ui`)
- **SHOULD have**: At least one `layer/*` tag (e.g., `layer/core`, `layer/interface`, `layer/entry-point`)
- **MAY have**: `pattern/*` tags for design patterns used (e.g., `pattern/strategy`)

**Concept Files** (`.md` in `obsidian/`):

```yaml
---
tags: [type/concept, domain/*, layer/*]
---
```

- **MUST have**: `type/concept`
- **SHOULD have**: Domain and layer tags matching related code

**Pattern Files** (`.md` in `obsidian/`):

```yaml
---
tags: [type/pattern, category/*]
---
```

- **MUST have**: `type/pattern`
- **SHOULD have**: `category/*` (e.g., `category/behavioral`, `category/solid-principles`)

**Index Files** (like `README.md`):

```yaml
---
tags: [type/index]
---
```

### Tag Hierarchies

Common hierarchies used:

- `type/*` - File classification (code-file, concept, pattern, index)
- `domain/*` - Problem domain (mathematics, ui, validation)
- `layer/*` - Architecture layer (core, interface, entry-point)
- `pattern/*` - Design patterns (strategy, etc.)
- `category/*` - Pattern categories (behavioral, solid-principles)

## Wikilink Conventions

**CRITICAL**: Use relative path-based wikilinks to avoid filename conflicts and maintain clarity.

From **Python files** in `code/`:

```python
"""
Related: [[../obsidian/arithmetic-operations|Arithmetic Operations]]
Dependencies: [[calculator.py|Calculator Class]]  # Same directory
"""
```

From **Markdown files** in `obsidian/`:

```markdown
Implementation: [[../code/operations.py|Operations Module]]
Related: [[calculator-interface|Calculator Interface]]  # Same directory
```

**Path Rules**:

- Same directory: Use filename only (e.g., `[[calculator.py]]`)
- Different directory: Use relative path (e.g., `[[../obsidian/concept|Display]]`)
- This allows duplicate filenames in different folders without conflicts

## Python Code Structure

Python files use a special docstring format:

```python
"""
---
tags: [type/code-file, domain/mathematics, layer/core]
---

# Module Name

## Purpose
Brief description of what this module does.

## Related Documentation
- Concept: [[concept-file|Display Name]]
- Pattern: [[pattern-file|Display Name]]

## Dependencies
- [[other-code.py|Other Module]]
"""

# Regular Python code follows...
```

The docstring frontmatter is parsed by Obsidian when `.py` files are configured as markdown files.

## Common Commands

**Run the calculator**:

```bash
cd code
python main.py
```

**Check repository health**:

```bash
python janitor.py              # Scan for issues
python janitor.py --fix        # Auto-fix issues (with confirmation)
python janitor.py --fix --yes  # Auto-fix without confirmation
```

The janitor validates:

- All files have required YAML frontmatter tags
- Python docstrings follow the correct schema
- Files are in correct directories

**Open in Obsidian**:

1. Open Obsidian
2. Open this folder as a vault
3. Install "Custom File Extensions Plugin"
4. Configure plugin: Add `py` extension, set view type to "Markdown"
5. Restart Obsidian
6. Use Graph View to explore code-documentation relationships

## Working with This System

### Adding New Code

1. Create `.py` file in `code/`
2. Add frontmatter with required tags:
   - MUST: `type/code-file`
   - SHOULD: `domain/*`, `layer/*`
3. Use wikilinks in docstrings to reference:
   - Related concepts: `[[concept-name|Display]]`
   - Design patterns: `[[pattern-name|Display]]`
   - Other code: `[[filename.py|Display]]`

### Adding New Documentation

1. Create `.md` file in `obsidian/` (flat, no subdirectories)
2. Add frontmatter with required tags:
   - Concepts: `type/concept` + domain/layer tags
   - Patterns: `type/pattern` + category tag
3. Link to code implementations: `[[code-file.py|Display]]`
4. Link to related docs: `[[other-doc.md|Display]]`

### Maintaining the Graph

The knowledge graph relies on:

- **Tags**: For filtering and organization in graph view
- **Wikilinks**: For creating edges between nodes
- **Backlinks**: Automatically maintained by Obsidian

When you add wikilinks, both forward links and backlinks appear in the graph, creating bidirectional navigation.

## Philosophy

Code documentation should be **unified, not separated**. Instead of:

- Code in one place
- API docs in another
- Architecture docs elsewhere
- Design rationale lost

This system creates:

- Code files are graph nodes
- Documentation files are graph nodes
- Wikilinks create semantic relationships
- Tags enable multiple views of the same content
- Navigate from "why" to "how" to "what" seamlessly

The filesystem structure is minimal; tags and links provide the organization.
